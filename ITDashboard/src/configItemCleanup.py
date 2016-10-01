'''
Created on Apr 1, 2016


This module should be set to run after the configuration item list is pulled
and the alert information is also pulled.
This is designed to remove any configuration items that belong to a group that
should be displayed but no longer exist in Panopta.

@author: Savanna Baxter
@author: McAkinyi Mboya
@author: Jay Patel
@author: Carl Smith
'''

from urllib2 import urlopen, Request
import json
import boto3
import config

'''
Removes the outdated resources from the dynamoDB database
'''
def cleanDatabase():
    # configuration information to connect to AWS DynamoDB database
    aws_access_key_id = config.aws_aki
    aws_secret_access_key = config.aws_sak
    table_name = config.tableName
    region_name = config.regionName
    dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
     
    # perform scan operation on the table   
    table = dynamodb.Table(table_name)
    responseDB = table.scan();
    
    # holds a list of all serverKeys present in the database
    serverKeyList = []
        
    # add all the keys that exist in the DynamoDB databaes into the list
    for item in responseDB['Items']:
        serverKeyList.append(item['serverKey'])

    # scan panopta for most recent server and key information iteratively by group
    # if a server key found in panopta matches one of the list it will be removed from the
    # list and no longer marked for deletion
    for key in config.serverGroups.iteritems():
        try:
            reqURL = 'https://api2.panopta.com/v2/server_group/' + key[0] + '/server?limit=0&offset=0'
            request = Request(reqURL)
            request.add_header(config.panoptaHeader, config.panoptaKey)
            responsePanopta = urlopen(request)
            json_obj = json.load(responsePanopta)
            
            for i in json_obj['server_list']:
                serverKeyList.remove(i['server_key'])

        except Exception, e:
            # handles the 404 errors if any group in the config file was deleted on panopta
            continue
    
    try:
        for serverKey in serverKeyList:
            table.delete_item(
                Key={
                    'serverKey': serverKey,
                }
            )
    except Exception, e:
        print e
        return 400 # error code for deletion failure
    
    print 'Configuration Item Cleanup Complete'
    return 200 # process successful