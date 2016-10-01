'''
Created on Feb 3, 2016

@author: Savanna Baxter
@author: McAkinyi Mboya
@author: Jay Patel
@author: Carl Smith

Module responsible for getting all of the sas functions
the user has the option of just displaying them to the console
or pushing them to the AWS DynamoDB service

'''

from urllib2 import urlopen, Request
import json
import boto3
import config

panoptaHeader = config.panoptaHeader # Panopta API Key Header Name
panoptaKey = config.panoptaKey # Panopta API Key
aws_aki = config.aws_aki # AWS Access Key ID
aws_sak = config.aws_sak # AWS Secret Access Key

# This class is responsible for pulling the active server list via the 
# Panopta API and then putting them onto the DynamoDB table SASResources
# it will populate an empty table and update tables if a device is added to the
# active servers list on Panopta
#
# return 200 successful connection both both AWS and Panopta services and 
# successfully pushed the data to the DB
#
# return 400 There was a connection or data processing error
def serverDBPopulator():    
    try:
        request = Request('https://api2.panopta.com/v2/server?limit=0&offset=0')
        request.add_header(panoptaHeader, panoptaKey)
        
        response = urlopen(request)
        json_obj = json.load(response)
        
        aws_access_key_id = aws_aki
        aws_secret_access_key = aws_sak
        table_name = config.tableName
        region_name = config.regionName

        dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
        
        table = dynamodb.Table(table_name)
        
        # Iterates through the json response from the API and writes the data to the DB
        with table.batch_writer() as batch:
            for i in json_obj['server_list']:
                groupNum = getServerGroup(i['server_group'])
                if groupNum in config.serverGroups:
                    batch.put_item(
                        Item={
                            'serverKey' : i['server_key'], # Primary Key
                            'resourceName': i['name'],
                            'FQDN' : i['fqdn'],
                            'serverGroup' : config.serverGroups[groupNum],
                            'serverGroupID' : groupNum,
                            'time_stamp' : 'NULL',
                            'severity' : 'NULL',
                            'outage_type' : 'NULL',
                            'outage_status' : 'up',
                            'UpdateURL' : i['url'],
                            'chartID' : generateChartID(groupNum, i['name'])
                        }
                    )
                else: # skip non monitored grouos
                    continue
                
        print 'DynamoDB Transfer Successful'
        
        return 200 # Successfully Connected
    except Exception as e: 
        print(e)
        return 400 # Connection Error

def generateChartID(groupNum, resourceName):
    combined = resourceName + groupNum
    removeDot = combined.replace('.','')
    removeHyphen = removeDot.replace('-','')
    removeUnderscore = removeHyphen.replace('_','')
    removeSpace = removeUnderscore.replace(' ','')
    return removeSpace

# Helper function to break the URL into parts and return the
# final element of the path
def getServerGroup(url):
    try:
        urlElements = url.split('/')
        return urlElements.pop()
    except Exception as e:
        print(e)
        return 'urlParseError'
        

# Trimmed down function of serverDBPopulator this is only responsible for
# calling the Panopta API and getting a list of active devices to print on the 
# console, for debugging purposes.
# return 200 successful connection to Panopta services and 
# successfully pushed the data to the DB
#
# return 400 There was a connection or data processing error
def serverLister():
    try:
        request = Request('https://api2.panopta.com/v2/server?limit=0&offset=0')
        request.add_header(panoptaHeader, panoptaKey)
                
        response = urlopen(request)
        json_obj = json.load(response)
        
        print 'List of Servers'
        
        for i in json_obj['server_list']:
            # Check to see if monitored group before printing
            groupNum = getServerGroup(i['server_group'])
            if groupNum == 'urlParseError':
                return groupNum
            if groupNum in config.serverGroups:
                print '-----------------------------------------'
                print 'Server Name:        ' + i['name']
                print 'Server FQDN:        ' + i['fqdn']
                print 'Server Key:         ' + i['server_key']
                print 'Server Group Name:  ' + config.serverGroups[groupNum]
                print 'Server Group ID:    ' + groupNum
            else: # skip this interation not a monitored group
                continue
        print '-----------------------------------------'
        return 200 # Successfully Connected
    except Exception as e: 
        print(e)
        return 400 # Connection Error