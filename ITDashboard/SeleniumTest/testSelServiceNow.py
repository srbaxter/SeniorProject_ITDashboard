'''
Created on Mar 15, 2016

@author: Carl
'''
import unittest
from selenium import webdriver


class Test(unittest.TestCase):


#sets up a webdrive of Firefox which is the browser that is used right now
    def setUp(self):
        self.driver = webdriver.Firefox()
        #driver = self.driver
        #driver.get("http://127.0.0.1:5000/servers")

    #This is just an example of a working Selenium test to go to the page
    def testTrySel(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        
        
    #test the link to ServiceNow
    def testLinktoSN(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/x")
        self.assertIn("SAS Network Monitoring Dashboard", driver.title)
        window_before = driver.window_handles[0]
        driver.find_element_by_id("p2_segment0").click()
        #click the link to SN
        driver.find_element_by_link_text("ServiceNow").click()
        #when the link is click it opens a new window so it is needed to be switched to
        window_after = driver.window_handles[1]
        driver.implicitly_wait(10)
        driver.switch_to_window(window_after)
        #check the title
        self.assertIn("ServiceNow", driver.title)
        driver.close()
        driver.switch_to_window(window_before)

    #close the webdriver
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()