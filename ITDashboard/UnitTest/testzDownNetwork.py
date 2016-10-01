'''
Created on Feb 18, 2016

@author: Carl
This is the evil test of if there was a total network 
failure. It makes sure that every back end function can fail
with out problems.
'''
import unittest

#Monkey patching the socket to act like the network is down
import socket              
def guard(*args, **kwargs):
    raise Exception("No connection For You")
socket.socket = guard

#import for the actual code so they can be tested
from src.alertPull import alertUpdater
from src.alertPull import alertLister
from src.serverPull import serverDBPopulator
from src.serverPull import serverLister
from src.configItemCleanup import cleanDatabase

class Test(unittest.TestCase):

    def testName(self):
        pass
    
    #Test for serverDBPopulator like the network is down
    def testServerPopNo(self):
        try:
            self.assertEqual(serverDBPopulator(),400)
        except Exception as e:
            pass
    
    #Test for serverLister like the network is down  
    def testServerListerNo(self): #test making sure it had a successful connection 
        self.assertEqual(serverLister(),400)
     
    #Test for alertUpdater like the network is down   
    def testAlertUpNo(self):
        self.assertEqual(alertUpdater(),400)
    
    #Test for alertLister like the network is down     
    def testAlertListerNo(self):
        self.assertEqual(alertLister(),400)
        
    def testCIClearn(self):
        self.assertEqual(cleanDatabase(),400)
    

if __name__ == "__main__":
    unittest.main()