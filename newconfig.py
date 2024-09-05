#!/usr/bin/python3
import openstack.cloud
import argparse
import re
import os
import openstack
import csv
import sys
conn = openstack.connect(cloud='openstack')
parser = argparse.ArgumentParser(description="Enter your IP address", epilog="Enter the IP address")
parser.add_argument('ip_address')
args = parser.parse_args()
#openstack.enable_logging(debug=True)

conn2 = conn.connect_as(username = os.environ.get('OS_USERNAME'), password = os.environ.get('OS_PASSWORD'))
cloud2 = conn.connect_as_project('7b9b3xxxxxxxxxxxxxxxxxa6e9a1cdc8bb07ae19000000000000000')

output_file = "result/output.csv"
#title = "Details are as below"

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

for i in cloud2.network.ips(floating_ip_address=args.ip_address):
  print(i)
  try:
    uuid = i.port_details['device_id']
    ins = cloud2.compute.get_server(uuid)
    print (ins)
    p = cloud2.identity.get_project(ins.project_id)
    print (p)
  except TypeError as t:
      print("IP Address is not Associated with VM")
 #     break
with open(output_file, 'w', newline='') as csvfile:
    sys.stdout = csvfile
    csv_writer = csv.writer(sys.stdout)
#    csvfile.write(title + '\n')

    # Write the header row
    csv_writer.writerow(['sep=#'])
    csv_writer.writerow(['Status#Name#Project#Owner'])
#    print ("instance State is:", i.status, i.name, i.project_id, p.owner)
#    print ("Instance Name Is:", i.name)
#    p = cloud2.identity.get_project(i.project_id)
#    print ("Project Name Is:", p.name)
 #  print (f"The Cost Center of {p.name}:", p.cost_center)
 #   print (f"The Owner of {p.name}:", p.owner)i
    try:
      print (ins.status, ins.name, p.name, p.owner if p.owner is not None else p.owner_name, sep='#')
    except AttributeError as e:
      if p.owner_name is not None:
        print(ins.status, ins.name, p.name, p.owner_name, sep='#')
    except NameError as n:
      print("No VM Details Found")
    
    # Additional handling steps can be added here

sys.stdout = sys.__stdout__
print("Instance Details have been saved to:", output_file)
