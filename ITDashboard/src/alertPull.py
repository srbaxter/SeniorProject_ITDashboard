'''
Created on Feb 3, 2016

Module is responsible for pulling the current list of active outages on the
SAS network, it will report and post (if specified) the downed server as well as
other diagnostic information

@author: Savanna Baxter
@author: McAkinyi Mboya
@author: Jay Patel
@author: Carl Smith
'''

from urllib2 import urlopen, Request
import json
import boto3
from boto3.dynamodb.conditions import Attr
import config

panoptaHeader = config.panoptaHeader # Panopta API Key Header Name
panoptaKey = config.panoptaKey # Panopta API Key
aws_aki = config.aws_aki # AWS Access Key ID
aws_sak = config.aws_sak # AWS Secret Access Key

# This function is responsible for pulling the current resources that are 
# displaying an offline status on the SAS from the Panopta API and then posting
# the current situation to a table on AWS DynamoDB. During processing it also
# takes care to look at the current table of offline devices and checks to see
# if any of those were resolved since the last function call, if they are it
# will be removed.
#
# return 200 successful connection both both AWS and Panopta services and 
# successfully pushed the data to the DB
#
# return 400 There was a connection or data processing error
def alertUpdater():
    try:
        request = Request('https://api2.panopta.com/v2/outage/active?limit=10&offset=0')
        request.add_header(panoptaHeader,panoptaKey)
        
        response = urlopen(request)
        json_obj = json.load(response)
        
        aws_access_key_id = aws_aki
        aws_secret_access_key = aws_sak
        table_name = config.tableName
        region_name =config.regionName

        dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
        
        table = dynamodb.Table(table_name)
        
        #A query to remove resolved outages
        try:
            removeResolved(table)  
        except Exception as a:
            print a
            print 'rr error'
            
        try:
            for i in json_obj['outage_list']:
                if i['server_group_id'] in config.serverGroups:
                    table.update_item(
                        Key={
                        'serverKey': getServerKey(i['server'])     
                        },
                        UpdateExpression="SET time_stamp = :ts, severity = :sev, outage_status = :stat, outage_type= :t",
                        ExpressionAttributeValues={
                            ':ts': i['start_time'],
                            ':sev': i['severity'],
                            ':stat': 'down',
                            ':t': i['type']
                        }
                    )
                else:
                    continue
        except Exception as e:
            print e
            
        print 'DynamoDB Transfer Successful'
            
        return 200 # Successful Connection
    except:
        return 400 # Connection Error

# Queries the activeOutage table for a list of devices that were stated to be
# offline. Uses the server's Panopta URL to check and see if its status has
# changed to up and if so remove it.
#
# table : table to perform actions on
# return success : if actions were successfully done
def removeResolved(table):
    resp = table.scan(
        FilterExpression=Attr('outage_status').eq('down')
    )
    
    for i in resp['Items']:
        request = Request(i['UpdateURL'])
        request.add_header(panoptaHeader, panoptaKey)
        response = urlopen(request)
        json_obj = json.load(response)
        if json_obj['current_state'] =='up': 
            table.update_item(
                Key={
                'serverKey': json_obj['server_key']     
                },
                UpdateExpression="SET time_stamp = :ts, severity = :sev, outage_status = :stat, outage_type= :t",
                ExpressionAttributeValues={
                    ':ts': 'NULL',
                    ':sev': 'NULL',
                    ':stat': 'up',
                    ':t': 'NULL'
                }
            )            
    return 'Success'
            
# This function addresses the data the issue that the server_key that uniquely
# identifies the servers in the tables is not present in the active outages
# return data, it takes the severs Panopta API URLs and gets its key
def getServerKey(url):
        request = Request(url)
        request.add_header(panoptaHeader, panoptaKey)
        response = urlopen(request)
        json_obj = json.load(response)
        return json_obj['server_key']

# A trimmed down function of alertUpdater it just contants the Panopt API and 
# prints the contents of a active outages get command
#
# return 200 successful connection both both AWS and Panopta services and 
# successfully pushed the data to the DB
#
# return 400 There was a connection or data processing error
def alertLister():
    try:
        request = Request('https://api2.panopta.com/v2/outage/active?limit=0&offset=0')
        request.add_header(panoptaHeader, panoptaKey)
        
        response = urlopen(request)
        json_obj = json.load(response)
        
        print 'Current Offline Servers'
        
        for i in json_obj['outage_list']:
            if i['server_group_id'] in config.serverGroups:
                print '----------------------------------'
                print 'Server Key       ' + getServerKey(i['server'])
                print 'Server Name:     ' + i['server_name']
                print 'Server FQDN:     ' + i['server_fqdn']
                print 'Server Group:    ' + i['server_group_name']
                print 'Server Group ID: ' + i['server_group_id']
                print 'Timestamp:       ' + i['start_time']
                print 'Severity:        ' + i['severity']
                print 'Type:            ' + i['type']
                print 'Status:          ' + i['status']
                print 'Update URL       ' + i['server']
            else:
                continue
            
        print '----------------------------------'
        return 200 # Successful Connection
    except:
        return 400 # Connection Error