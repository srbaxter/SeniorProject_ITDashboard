'''
Created on Feb 18, 2016

@author: Savanna Baxter
@author: McAkinyi Mboya
@author: Jay Patel
@author: Carl Smith
'''
from flask import Flask, render_template
from time import strftime, gmtime, strptime, mktime
import boto3
from boto3.dynamodb.conditions import Attr
import src.config

'''
NOTE: IN VERSION DEPLOYED TO ELASTIC BEANSTALK REMOVE ALL 'src.' 
FROM ALL config REFERENCES

ALSO CHANGE @app.route("/x") to @app.route("/"), IT NEEDS TO STAY /X
IN LOCAL VERSION FOR SELENIUM TESTS TO WORK
'''

application = app = Flask(__name__)
    
@app.route("/x")
def chart():
    aws_access_key_id = src.config.aws_aki
    aws_secret_access_key = src.config.aws_sak
    #serverPull.serverDBPopulator()
    #alertPull.alertUpdater()
    table_name = src.config.tableName
    region_name = src.config.regionName
    dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
        
    table = dynamodb.Table(table_name)
    response = table.scan()
    
    playSound = alertSoundSetter(table)
    with app.app_context():
        return render_template('d3donutchart.html', data = response, groups = src.config.serverGroups, sound = playSound)

# Scans the table for any configuration items that are down
# if it finds one it checks the timestamp for the outage and if
# it is less than our refresh rate it will send a singal for the
# webpage to make an audible alert
def alertSoundSetter(table):
    outageResponse = table.scan(
        FilterExpression=Attr('outage_status').eq('down') # scan for all items with the status down
    )
    
    timeNow = strftime("%a, %d %b %Y %H:%M:%S", gmtime()) # current time as string
    timeNow_struct_time = strptime(timeNow,"%a, %d %b %Y %H:%M:%S")# current time to workable time object
    
    for item in outageResponse['Items']: # iterate through all of the items whose current status is down
        outageTimestamp = item['time_stamp']
        outageTimestamp = outageTimestamp.rsplit(' ', 1)[0] # removes last token -0000
        outageTimestamp_struct_time = strptime(outageTimestamp, "%a, %d %b %Y %H:%M:%S") # changes time time to a workable object
        if (outageTimestamp_struct_time.tm_mday == timeNow_struct_time.tm_mday) and (outageTimestamp_struct_time.tm_mon == timeNow_struct_time.tm_mon) and (outageTimestamp_struct_time.tm_year == timeNow_struct_time.tm_year):
            secDiff  = (mktime(timeNow_struct_time) - mktime(outageTimestamp_struct_time)) # gets the second difference between now and the outage
            #print 'Seconds Difference %f' % secDiff
            if secDiff <= src.config.notificationThreshold: #considered a new alert then set sounds to play
                #print 'BEEP BEEP BEEP!' #set the trigger should be a return
                return 'true'
    return 'false'

if __name__ == "__main__":
    application.jinja_env.add_extension('jinja2.ext.loopcontrols')
    application.run()