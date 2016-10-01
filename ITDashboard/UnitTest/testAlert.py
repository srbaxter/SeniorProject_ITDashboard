'''
Created on Feb 4, 2016

@author: Carl
'''
import unittest
import boto3
import json
from urllib2 import urlopen, Request
from src.alertPull import alertUpdater
from src.alertPull import removeResolved
from src.alertPull import getServerKey
from src.alertPull import alertLister
import src.config

panoptaHeader = src.config.panoptaHeader # Panopta API Key Header Name
panoptaKey = src.config.panoptaKey # Panopta API Key
aws_aki = src.config.aws_aki # AWS Access Key ID
aws_sak = src.config.aws_sak # AWS Secret Access Key

class Test(unittest.TestCase):

    def testName(self):  #a passing test
        pass
    
    #alertUpdater
    def testalertUp(self):
        self.assertEqual(alertUpdater(),400)
    
    #removeResolved
    
    #getServerKey
    def testUrlKey(self):
        self.assertEqual(getServerKey("https://api2.panopta.com/v2/server/752535"), "v5qk-96cg-8cbv-63py")
        
    def testRemoveRes(self):
        request = Request('https://api2.panopta.com/v2/outage/active?limit=0&offset=0')
        request.add_header(panoptaHeader,panoptaKey)
        
        response = urlopen(request)
        json_obj = json.load(response)
        aws_access_key_id = aws_aki
        aws_secret_access_key = aws_sak
        table_name ='activeOutages'
        region_name ='us-west-2'
        dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
        
        table = dynamodb.Table(table_name)
        self.assertEqual(removeResolved(table),'Success')
    
    #alertLister
    def testIfConnection(self): #test making sure it had a successful connection 
        self.assertEqual(alertLister(),200)


if __name__ == "__main__":
    unittest.main()