'''
Created on Feb 3, 2016

@author: Savanna Baxter
@author: McAkinyi Mboya
@author: Jay Patel
@author: Carl Smith

Quick interface for demo purposes

'''

import alertPull
import serverPull
import configItemCleanup

menu = {}
menu['1']="View All Servers" 
menu['2']="Populate DynamoDB with All Servers"
menu['3']="View Active Outages"
menu['4']="Update DynamoDB with Active Outages"
menu['5']="Clean Up Configuration Items in Database"
menu['6']="Exit"

print '**********************************************************'
print 'For the DynamoDB functions to work (option 2, 4, and 5),'
print 'there needs to exists a table in DynamoDB called'
print 'SASResourcesTest and a need to have a primary'
print 'key called serverKey'
print '**********************************************************'

while True: 
    options=menu.keys()
    options.sort()
    for entry in options: 
        print entry, menu[entry]

    selection=raw_input("Please Select:") 
    if selection =='1': 
        serverPull.serverLister()
    elif selection == '2':
        serverPull.serverDBPopulator()
    elif selection == '3': 
        alertPull.alertLister()
    elif selection == '4':
        alertPull.alertUpdater()
    elif selection == '5':
        configItemCleanup.cleanDatabase()
    elif selection == '6':
        break
    else: 
        print "Unknown Option Selected!" 