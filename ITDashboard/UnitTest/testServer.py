'''
Created on Feb 4, 2016

@author: Carl
'''
import unittest
from src.serverPull import serverLister
from src.serverPull import serverDBPopulator
from src.serverPull import getServerGroup

class Test(unittest.TestCase):


    def testName(self): #a passing test  
        pass

    #serverDBPopulator
    def testConnectandPopulate(self): #test making sure it had a successful connection and inputs info into database 
        self.assertEqual(serverDBPopulator(),200)
        
    #getServerGroup
    def testValidUrl(self):
        self.assertEqual(getServerGroup("https://api2.panopta.com/v2/server_group/50893"),"50893")
    
    def testInvaildUrlNotString(self):
        self.assertEqual(getServerGroup(5),"urlParseError")
    
    #serverLister
    def testIfConnection(self): #test making sure it had a successful connection 
        self.assertEqual(serverLister(),200)
        

if __name__ == "__main__":
    unittest.main()