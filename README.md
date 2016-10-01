# IT Dashboard


##Deploying to Elastic Beanstalk
In your version deployed to Elastic Beanstalk, remove all 'src.' from all 'config' references 

Also, change @app.route("/x") to @app.route("/"). It needs to stay '/x' in the local version for Selenium tests to work


##Config File
Create a new Python file with the variables:
* panoptaHeader
* panoptaKey
* aws_aki
* aws_sak
* serverGroups
* notificationThreshold
* table_name
* region_name

Use .gitignore to make this file inaccessible to the public
