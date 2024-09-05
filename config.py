#!/usr/bin/python3

#!/usr/bin/python3
import openstack.cloud
import argparse
import re
import os
import openstack
conn = openstack.connect(cloud='openstack')
parser = argparse.ArgumentParser(description="Enter your IP address", epilog="Enter the IP address")
parser.add_argument('ip_address')
args = parser.parse_args()
#openstack.enable_logging(debug=True)
conn2 = conn.connect_as(username='sunilka', password= os.environ.get('OS_PASSWORD'))
cloud2 = conn.connect_as_project('7b9b3c86a8ab4a6e9a1cdc8bb07ae190')

#validating the Ip address of the vm instance

def is_valid_ip(ip):
    ip_regex = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    return re.match(ip_regex, ip) is not None

def main():
    parser = argparse.ArgumentParser(description='Validate IP Address')
    parser.add_argument('ip_address', type=str, help='IP address to validate')
    args = parser.parse_args()

    if is_valid_ip(args.ip_address):
        print(f'{args.ip_address}')
    else:
        print(f'{args.ip_address} is not a valid IP address.')

if __name__ == '__main__':
    main()

for i in cloud2.network.ips(floating_ip_address=args.id):
  uuid = i.port_details['device_id']
  i = cloud2.compute.get_server(uuid)
  print ("instance State is:", i.status)
  print ("Instance Name Is:", i.name)
  p = cloud2.identity.get_project(i.project_id)
  print ("Project Name Is:", p.name)
  print (f"The Cost Center of {p.name}:", p.cost_center)
  print (f"The Owner of {p.name}:", p.owner)
