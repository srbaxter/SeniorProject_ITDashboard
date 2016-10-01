'''
Created on Feb 29, 2016

@author: Carl
'''
import unittest
import os
from selenium import webdriver

#same test just in Chrome
class Test(unittest.TestCase):

    #sets up a webdrive of Chrome which is the browser that is used right now
    def setUp(self):
        chromedriver = "C:\Users\Carl\Documents\senior design\chromedriver_win32\chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

    #This is just an example of a working Selenium test all it does is go to python.org and check header
    @unittest.skip("Works but takes 5 min to run")
    def testTrySel(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        
        
    #A test that goes to the page and checks the title
    def testchrom(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
        driver.implicitly_wait(10)
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        
      
    #Opens one of the donut slices and then checks if that slices was opened     
    def testchromexp(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
        driver.implicitly_wait(10)
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        driver.find_element_by_id("p2_segment0").click()
        ifvis2 = driver.find_element_by_id("supportsascomextratest50893").value_of_css_property('display')
        self.assertEqual(ifvis2,"block")
        
    
    #checks the color of different donut slices     
    def testorder(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
        driver.implicitly_wait(10)
        self.assertIn("", driver.title)
        rgb = driver.find_element_by_id("p3_segment0").value_of_css_property('fill') # first is red then the second is green 
        self.assertEqual(rgb,"rgb(255, 0, 0)")
        rgb = driver.find_element_by_id("p3_segment1").value_of_css_property('fill')
        self.assertEqual(rgb,"rgb(0, 255, 0)")
        
    
    #opens a donut slice then opens a second donut slice and makes sure the first slice closes     
    def testOpen(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
        driver.implicitly_wait(10)
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        
        driver.find_element_by_id("p2_segment1").click() # something wrong with finding this 
        driver.implicitly_wait(10)
        ifvis1 = driver.find_element_by_id("wwwsascom50893").value_of_css_property('display')
        self.assertEqual(ifvis1,"block")
        
        driver.find_element_by_id("p2_segment0").click()
        driver.implicitly_wait(10)
        ifvis2 = driver.find_element_by_id("supportsascomextratest50893").value_of_css_property('display')
        self.assertEqual(ifvis2,"block")
        
        ifvis1 = driver.find_element_by_id("wwwsascom50893").value_of_css_property('display')
        self.assertEqual(ifvis1,"none")


    #close the webdriver
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()