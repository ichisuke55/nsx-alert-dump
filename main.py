import os
import json
import csv
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    'Content-Type': 'application/json',
}

origin_response = requests.get(
        f"https://{os.environ['NSX_FQDN']}/api/v1/events", timeout=5, headers=headers, verify=False,
        auth=requests.auth.HTTPBasicAuth(f"{os.environ['NSX_USER']}", f"{os.environ['NSX_PASSWORD']}"))
origin_data = origin_response.json()

headers.update({'Accept-Language': 'ja-JP'})
jp_response = requests.get(
        f"https://{os.environ['NSX_FQDN']}/api/v1/events", timeout=5, headers=headers, verify=False,
        auth=requests.auth.HTTPBasicAuth(f"{os.environ['NSX_USER']}", f"{os.environ['NSX_PASSWORD']}"))
jp_data = jp_response.json()

with open('./dump.csv', 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    header = ['EVENT_TYPE', 'SUMMARY(EN)', 'SUMMARY(JP)', 'DESCRIPTION(EN)', 'DESCRIPTION(JP)', 'OID']
    writer.writerow(header)
    for _, o in enumerate(origin_data['results']):
        for _, j in enumerate(jp_data['results']):
            if o['event_type'] == j['event_type']:
                # true_oid
                writer.writerow([o['event_type'], o['summary'], j['summary'],
                    o['description'], j['description'], o['event_true_snmp_oid']])
                # false_oid
                writer.writerow([o['event_type'], o['summary'], j['summary'],
                    o['description_on_clear'], j['description_on_clear'], o['event_false_snmp_oid']])

