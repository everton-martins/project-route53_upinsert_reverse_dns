import boto3, sys

# Initial parameters
OLD_IP  = sys.argv[1]
NEW_IP  = sys.argv[2]
ENVTYPE = sys.argv[3]

# ZoneIDs
if ENVTYPE=='prd':
    ZONEID='/hostedzone/Z38ERPC71LLE7'
    PROFILE='default'
elif ENVTYPE=='dev':
    ZONEID='/hostedzone/Z30N255VLTE3FX'
    PROFILE='shr'
elif ENVTYPE=='hlg':
    ZONEID='/hostedzone/Z1N9HWA1P14UQ1'
    PROFILE='shr'


# boto initialization
s = boto3.Session(profile_name=PROFILE)
client = s.client('route53')



# Main
#########

DNS_NAME=[]
paginator = client.get_paginator('list_resource_record_sets')
source_zone_records = paginator.paginate(HostedZoneId=ZONEID, PaginationConfig={'MaxItems':5000} )

# Search records
for record_set in source_zone_records:
     for record in record_set['ResourceRecordSets']:
         if record['Type'] == 'A' and 'ResourceRecords' in record and record['ResourceRecords'][0]['Value']==OLD_IP:
             DNS_NAME.append({ 'Name': record['Name'], 'TTL': record['TTL'] })

#Change Records
for NAME in DNS_NAME:
    response = client.change_resource_record_sets(
                     HostedZoneId=ZONEID,
                     ChangeBatch={
                         'Changes': [{
                             'Action': 'UPSERT',
                             'ResourceRecordSet': {
                                 'Name': NAME['Name'],
                                 'Type': 'A',
                                 'TTL': NAME['TTL'],
                                 'ResourceRecords': [{'Value': NEW_IP}]
                          }}]})

#End
