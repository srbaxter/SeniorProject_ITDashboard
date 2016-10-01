'''
Created on Mar 22, 2016

@author: Carl
'''
import unittest
from selenium import webdriver
import time

#used for testing and getting them to work
class Test(unittest.TestCase):


    def setUp(self):
        self.driver = webdriver.Firefox()             
     
    
    #A test of the title of the page to make sure it's the right page   
    def testTrySel(self):
        driver = self.driver
        driver.get("http://testenv.us-west-2.elasticbeanstalk.com/")
        driver.implicitly_wait(10)
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        
         
    #test that the page auto refreshes every 5 min
    def testAutoRefresh(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
        driver.implicitly_wait(10)
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        driver.find_element_by_id("p2_segment0").click()
        driver.implicitly_wait(10)
        #check a slice is expanded
        try:
            driver.find_element_by_link_text("ServiceNow")
        except Exception:
            self.fail("It should be found and if this is printed it was not found")
        #waits just over 5 min
        time.sleep(505)
        driver.implicitly_wait(10)
        #makes sure that the slice is no longer expanded
        try:
            driver.find_element_by_link_text("ServiceNow")
            self.fail("found when not their")
        except Exception:
            pass
        
    
    #Test the order of the slices. They should have red(down) ones first    
    def testorder(self):
        driver = self.driver
        driver.get("http://testenv.us-west-2.elasticbeanstalk.com/")
        driver.implicitly_wait(10)
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
                
        qws = 1
        for x in xrange(12):
            pieplce = "p3_segment" + str(x)
            print pieplce
            if qws==1:
                rgb = driver.find_element_by_id(pieplce).value_of_css_property('fill')
                if rgb != "rgb(255, 0, 0)":
                    qws = 0
                else:
                    self.assertEqual(rgb,"rgb(255, 0, 0)")
                
            if qws==0:
                rgb = driver.find_element_by_id(pieplce).value_of_css_property('fill')
                self.assertEqual(rgb,"rgb(0, 255, 0)")
                
    
    # tries to open a slices           
    def testsselect(self):
        driver = self.driver
        driver.get("http://testenv.us-west-2.elasticbeanstalk.com/")
        driver.implicitly_wait(10)
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        #click a pie slice this is the left one of the first pie
        driver.find_element_by_id("p2_segment0").click()
        driver.implicitly_wait(10)
        #checks for the link
        try:
            driver.find_element_by_link_text("ServiceNow")
        except Exception:
            self.fail("It should be found and if this is printed it was not found")


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()