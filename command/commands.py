# get subnets

nimbula-admin-get-subnet = "nimbula-admin -a api -u user -p pwd get configpoint  /network/clusters -fjson"
out, _ = run_command(cmd)
try:
    json_out = json.loads(out)
except Exception as e:
    log.error("Failed to load json: %s, raised : %s", naoutput, e)
    raise Exception

subnets = json_out['list'][0]['value']


nimbula-admin-chk-cluster-added = "nimbula-admin -a api -u user -p pwd get configpoint /network/clusters/'subnet' -fjson"


nimbula-admin-list-node = "nimbula-admin -a api -u user -p pwd list node / -f json"
 
output, err = run_command(cmd)
      try:
          json_na = json.loads(output)
      except Exception as e:
          log.error("Failed to load json: %s, raised : %s", naoutput, e)
          raise Exception

      num_nodes_in_subnet = 0
      endpoints = []
      for node in json_na['list']:
          if allsubnet:
              if node['status'] != 'dead':
                  num_nodes_in_subnet += 1
                  endpoints.append(node['endpoint'])
          else:
S>                if node['cluster'] == cluster_subnet and node['status'] != 'dead':
                  num_nodes_in_subnet += 1
                  endpoints.append(node['endpoint'])


nimbula-admin-chk-pxe-enabled = "nimbula-admin -a api -u user -p pwd get configpoint /services/pxe/enabled -F value"


nimbula-admin-add-cluster = "nimbula-admin add cluster -a api -u user -p pwd" \
                "subnet instance_subnet " \
                "--dhcp {5} --dhcpstart {6} "\
                "--dhcpend {7} --router {8} --adminaddr {9} --dns {10} "\
                "--dns_ips {11} --api_dns_ips {12}"
                "--profile {0}"
                "--over_provisioning {0}"
                "--external_snmp_trapsink {0}"


nimbula-admin-chk-cluster-add = "nimbula-admin -a {0} -u {1} -p {2}"
                                "get configpoint /network/clusters/{subnet}/admin_cluster"
        return 'true' if added, "false" not added

nimbula-admin-mark-not-admin = "nimbula-admin -a {0} -u {1} -p {2} add " \
                r"configpoint /network/clusters/{0}/admin_cluster {".": false}"


nimbula-admin-add-properties = "nimbula-admin -a {0} -u {1} -p {2} add " \
                r"configpoint /network/clusters/{0}/properties "



