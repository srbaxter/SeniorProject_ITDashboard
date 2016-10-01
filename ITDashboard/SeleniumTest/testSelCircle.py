'''
Created on Mar 17, 2016

@author: Carl
'''
import unittest
from selenium import webdriver
import time

class Test(unittest.TestCase):


    def setUp(self):
        self.driver = webdriver.Firefox()


    #A basic test to get to the page and test the title of the page
    def testTrySel(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
        driver.implicitly_wait(10)
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        
        
    #After getting to the page, clicks a donut slice to expand it 
    #after the expand, looks for the ServiceNow link to check
    def testsselect(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
        driver.implicitly_wait(10)
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        #click a donut slice. this is the left one of the first pie
        driver.find_element_by_id("p2_segment0").click()
        driver.implicitly_wait(10)
        #checks for the link
        try:
            driver.find_element_by_link_text("ServiceNow")
        except Exception:
            self.fail("It should be found and if this is printed it was not found")
            
    
    #a basic test of the color of a slice    
    def testcolor(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
        driver.implicitly_wait(10)
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        rgb = driver.find_element_by_id("p2_segment0").value_of_css_property('fill')
        self.assertEqual(rgb,"rgb(0, 255, 0)")
        
        
    #test that slices are order by failure/color with fail first  
    def testorder(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
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
                
        
    #Expands a slice check that it opens then opens a second slice
    #makes sure the second slice expands and the first is no longer expanded    
    def testOpen(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
        driver.implicitly_wait(10)
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        
        driver.find_element_by_id("p2_segment1").click() # something wrong with finding this 
        driver.implicitly_wait(10)
        #name of the expanded element
        ifvis1 = driver.find_element_by_id("wwwsascom50893").value_of_css_property('display')
        self.assertEqual(ifvis1,"block") #value it should have when expanded 
        
        driver.find_element_by_id("p3_segment0").click()
        #name of the expanded element
        ifvis2 = driver.find_element_by_id("sasprodservicenowping26981").value_of_css_property('display')
        self.assertEqual(ifvis2,"block")
        
        ifvis1 = driver.find_element_by_id("wwwsascom50893").value_of_css_property('display')
        self.assertEqual(ifvis1,"none") #value when hidden
        
        
    @unittest.skip("sound is only made when something goes down")
    #check that when a CI goes down there is an audible alert made      
    def testsSound(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        try:
            driver.find_element_by_id("soundmade")
        except Exception:
            self.fail("sound not found")
        
    
    @unittest.skip("Works but takes 5 min to run")
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


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()