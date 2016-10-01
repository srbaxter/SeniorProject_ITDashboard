'''
Created on April 4, 2016

This is the function that will uploaded to lambda in order for the events to
automatically occur

How to use:
1. Zip this file up with alertPull.py, config.py, configItemCleanup.py,
   and serverPull.py
2. Name the ZIP file lambdaFunc (arbitrary, can be named anything)
3. Create a lambda function on AWS and choose the upload ZIP file option
   and upload the ZIP you just created
4. In function configuration set the event to be a CRON timer on 5 minutes.


@author: Savanna Baxter
@author: McAkinyi Mboya
@author: Jay Patel
@author: Carl Smith
'''

import alertPull
import serverPull
import configItemCleanup

def lambda_handler(event, context):
    serverPull.serverDBPopulator()
    alertPull.alertUpdater()
    configItemCleanup.cleanDatabase()