'''
Created on Apr 4, 2016

@author: Carl
'''
import unittest
from src.configItemCleanup import cleanDatabase
import src.config

panoptaHeader = src.config.panoptaHeader # Panopta API Key Header Name
panoptaKey = src.config.panoptaKey # Panopta API Key
aws_aki = src.config.aws_aki # AWS Access Key ID
aws_sak = src.config.aws_sak # AWS Secret Access Key


class Test(unittest.TestCase):


    def testName(self):
        pass
    
    def testCIClearn(self):
        self.assertEqual(cleanDatabase(),200)


if __name__ == "__main__":
    unittest.main()