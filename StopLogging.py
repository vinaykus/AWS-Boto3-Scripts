# -*- coding: utf-8 -*-

'''

Author      : Shalini Sasidharan
Description : This script will disable logging for all the trails in the specified region
			  that currently have the logging feature enabled.

INPUT PARAMETERS:

	aws_access_key_id           ** Required
    aws_secret_access_key       ** Required
    region_name                 ** Required
	

'''

import boto3


def stop_logging(aws_access_key_id, aws_secret_access_key, region_name):

	session = boto3.Session(region_name=region_name,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
	cloudtrail = session.client('cloudtrail')

	#Gets all the trails that are available in the specified region. Shadow trails are not included.
	trails = cloudtrail.describe_trails()['trailList'] 
	for trail in trails:
		cloudtrailARN=trail.get('TrailARN')
		# Disable logging for the trails which have logging enabled
		if cloudtrail.get_trail_status(Name=cloudtrailARN)['IsLogging'] == True:
			cloudtrail.stop_logging(Name=cloudtrailARN)
			print("Logging stopped for",format(cloudtrailARN))	
			
def main():
	stop_logging(<aws_access_key_id>, <aws_secret_access_key>, <region_name>) 
	

if __name__ == "__main__":
	main()