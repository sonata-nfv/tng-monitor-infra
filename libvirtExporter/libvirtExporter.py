from __future__ import print_function
import sys, os 
import argparse
import libvirt
import sched
import time
from prometheus_client import start_http_server, Gauge
from xml.etree import ElementTree


parser = argparse.ArgumentParser(description='libvirtExporter scrapes domains metrics from libvirt daemon')
parser.add_argument('-i','--scrape_interval', help='scrape interval for metrics in seconds', default= 5)
parser.add_argument('-uri','--uniform_resource_identifier', help='Libvirt Uniform Resource Identifier', default= "qemu:///system")

args = vars(parser.parse_args())
uri = args["uniform_resource_identifier"]


def report_libvirt_error():
    """Call virGetLastError function to get the last error information."""
    err = libvirt.virGetLastError()
    if if debug is None:
        return
    print('Error code:    '+str(err[0]), file=sys.stderr)
    print('Error domain:  '+str(err[1]), file=sys.stderr)
    print('Error message: '+err[2], file=sys.stderr)
    print('Error level:   '+str(err[3]), file=sys.stderr)
    if err[4] != None:
        print('Error string1: '+err[4], file=sys.stderr)
    else:
        print('Error string1:', file=sys.stderr)
    if err[5] != None:
        print('Error string2: '+err[5], file=sys.stderr)
    else:
        print('Error string2:', file=sys.stderr)
    if err[6] != None:
        print('Error string3: '+err[6], file=sys.stderr)
    else:
        print('Error string3:', file=sys.stderr)
    print('Error int1:    '+str(err[7]), file=sys.stderr)
    print('Error int2:    '+str(err[8]), file=sys.stderr)

def connect_to_uri(uri):
    conn = libvirt.open(uri)

    if conn == None:
        print('Failed to open connection to ' + uri, file = sys.stderr)

    return conn


def get_domains(conn):

    domains = []

    for id in conn.listDomainsID():
        dom = conn.lookupByID(id)

        if dom == None:
            print('Failed to find the domain ' + dom.name(), file=sys.stderr)
        else:
            domains.append(dom)

    if len(domains) == 0:
        print('No running domains in URI')
        return None
    else:
        return domains


def get_metrics_collections(metric_names, labels, stats):
    dimensions = []
    metrics_collection = {}

    for mn in metric_names:
        if type(stats) is list:
            dimensions = [[stats[0][mn], labels]]
        elif type(stats) is dict:
            dimensions = [[stats[mn], labels]]
        metrics_collection[mn] = dimensions

    return metrics_collection


def get_metrics_multidim_collections(dom, metric_names, device):

    tree = ElementTree.fromstring(dom.XMLDesc())
    targets = []

    for target in tree.findall("devices/" + device + "/target"): # !
        targets.append(target.get("dev"))

    metrics_collection = {}

    for mn in metric_names:
        dimensions = []
        for target in targets:
            labels = {'domain': dom.name(), 'resource_id': dom.UUIDString()}
            labels['target_device'] = target
            if device == "interface":
             stats = dom.interfaceStats(target) # !
            elif device == "disk":
                stats= dom.blockStats(target)
            stats = dict(zip(metric_names, stats))
            dimension = [stats[mn], labels]
            dimensions.append(dimension)
            labels = None
        metrics_collection[mn] = dimensions

    return metrics_collection


def add_metrics(dom, header_mn, g_dict):
    uuid = dom.UUIDString()
    labels = {'domain':dom.name(),'resource_id': uuid}
    metrics_collection = {}

    if header_mn == "libvirt_cpu_stats_":
        try:
            stats = dom.getCPUStats(True)
            metric_names = stats[0].keys()
            metrics_collection = get_metrics_collections(metric_names, labels, stats)
            unit = "_nanosecs"
        except:
            pass

    elif header_mn == "libvirt_mem_stats_":
        stats = dom.memoryStats()
        if ('available' in stats) and ('unused' in stats):
            mem_util = round(((float(stats['available'] - stats['unused'])) / float(stats['available']) * 100), 2)
            stats['mem_util'] = mem_util
        else:
            mem_util = float(-1.0)
        metric_names = stats.keys()

        metrics_collection = get_metrics_collections(metric_names, labels, stats)
        unit = ""

    elif header_mn == "libvirt_domain_info_":
        stats = dom.info()
        metric_names = \
            ['status',
             'max_mem',
             'used_mem',
             'vcpus',
             'total_cpu_time',
             'cpu_util']
        mystats = {}
        mystats['status'] = stats[0]
        mystats['max_mem'] = stats[1]
        mystats['used_mem'] = stats[2]
        mystats['vcpus'] = stats[3]
        mystats['total_cpu_time'] = stats[4] / 1000000000.
        mystats['cpu_util'] = -1
        now = time.time()
        if uuid in g_dict['last_value']:
            cpu_perc = float((mystats['total_cpu_time'] - g_dict['last_value'][uuid]['value'])/((now - g_dict['last_value'][uuid]['timestamp'])*mystats['vcpus']))
            cpu_perc = round(cpu_perc*100, 2)
            if (cpu_perc > 100):
                cpu_perc = 100.0
            mystats['cpu_util'] = cpu_perc
        g_dict['last_value'][uuid] = {'value':mystats['total_cpu_time'], 'timestamp': now}
        metrics_collection = get_metrics_collections(metric_names, labels, mystats)
        unit = ""

    elif header_mn == "libvirt_block_stats_":

        metric_names = \
        ['read_requests_issued',
        'read_bytes' ,
        'write_requests_issued',
        'write_bytes',
        'errors_number']

        metrics_collection = get_metrics_multidim_collections(dom, metric_names, device="disk")
        unit = ""

    elif header_mn == "libvirt_interface_":

        metric_names = \
        ['read_bytes',
        'read_packets',
        'read_errors',
        'read_drops',
        'write_bytes',
        'write_packets',
        'write_errors',
        'write_drops']

        metrics_collection = get_metrics_multidim_collections(dom, metric_names, device="interface")
        unit = ""

    for mn in metrics_collection:
        metric_name = header_mn + mn + unit
        dimensions = metrics_collection[mn]

        if metric_name not in g_dict.keys():

            metric_help = 'help'
            labels_names = metrics_collection[mn][0][1].keys()

            g_dict[metric_name] = Gauge(metric_name, metric_help, labels_names)

            for dimension in dimensions:
                dimension_metric_value = dimension[0]
                dimension_label_values = dimension[1].values()
                g_dict[metric_name].labels(*dimension_label_values).set(dimension_metric_value)
        else:
            for dimension in dimensions:
                dimension_metric_value = dimension[0]
                dimension_label_values = dimension[1].values()
                g_dict[metric_name].labels(*dimension_label_values).set(dimension_metric_value)
    return g_dict


def job(uri, g_dict, scheduler):
    domins = None
    try:
        conn = connect_to_uri(uri)
        domains = get_domains(conn)
    except:
        report_libvirt_error()
        pass

    headers_mn = ["libvirt_cpu_stats_", "libvirt_mem_stats_", \
                  "libvirt_block_stats_", "libvirt_interface_", "libvirt_domain_info_"]

    if domains is not None:
        for dom in domains:
            #print(dom.name() + ' ' + dom.UUIDString())
            if int(dom.info()[0]) != 1:
                continue

            for header_mn in headers_mn:
                g_dict = add_metrics(dom, header_mn, g_dict)

    conn.close()
    scheduler.enter((int(args["scrape_interval"])), 1, job, (uri, g_dict, scheduler))

def main():

    start_http_server(9091)

    g_dict = {}
    g_dict['last_value'] = {}
    scheduler = sched.scheduler(time.time, time.sleep)
    print('START:', time.time())
    scheduler.enter(0, 1, job, (uri, g_dict, scheduler))
    scheduler.run()

if __name__ == '__main__':
    main()