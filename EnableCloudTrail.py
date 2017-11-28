# -*- coding: utf-8 -*-

'''

Author      : Shalini Sasidharan
Description : This script will create a new trail with a custom trail name and a new s3 bucket for the storage of the logs.

INPUT PARAMETERS:

	AccountId                   ** Required
	aws_access_key_id           ** Required
    aws_secret_access_key       ** Required
    region_name                 ** Required
	cloudtrail_name				** Required

	
VERSION UPDATES:
	0.1 - Creating a cloudtrail with logging enabled.
	0.2 - Hashing of log files. Passing access keys as parameters.
	
'''

import boto3
from botocore.exceptions import ClientError
import random
import json


def enablecloudtrail(AccountId, aws_access_key_id, aws_secret_access_key, region_name, cloudtrail_name):

	session = boto3.Session(region_name=region_name,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)

	# Creating an S3 bucket
	
	try:

		s3 = session.client('s3')
		S3Bucket = 'cloudtrail-' + str(random.randint(11111,99999))
		s3.create_bucket(Bucket=S3Bucket, CreateBucketConfiguration={'LocationConstraint': region_name}, ACL='private')
    
	except ClientError as e:
	
		print(e.response['Error']['Message'])
    

	# Create the bucket policy

	bucket_policy = {
		"Version": "2012-10-17",
		"Statement": [
			{
				"Sid": "AWSCloudTrailAclCheck20150319",
				"Effect": "Allow",
				"Principal": {"Service": "cloudtrail.amazonaws.com"},
				"Action": "s3:GetBucketAcl",
				"Resource": "arn:aws:s3:::%s" % S3Bucket
			},
			{
				"Sid": "AWSCloudTrailWrite20150319",
				"Effect": "Allow",
				"Principal": {"Service": "cloudtrail.amazonaws.com"},
				"Action": "s3:PutObject",
				"Resource": "arn:aws:s3:::%s/AWSLogs/%s/*" % (S3Bucket, AccountId),
				"Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
			}
		]
	}



	# Convert the policy to a JSON string
	bucket_policy = json.dumps(bucket_policy)

	# Set the new policy on the given bucket
	s3.put_bucket_policy(Bucket=S3Bucket, Policy=bucket_policy)

	# Creating a new Trail

	#CloudTrailName = 'CloudTrail-Test2'
	ct = session.client('cloudtrail')
	
	try:

		res = ct.create_trail(
				Name=cloudtrail_name,
				S3BucketName=S3Bucket,
				IncludeGlobalServiceEvents=True,
				IsMultiRegionTrail=True,
				EnableLogFileValidation=True
			)
				
	except ClientError as e:

		print(e.response['Error']['Message'])
		
	else:

	    # Enable logging on the new trail
		CloudTrailARN = res['TrailARN']
		ct.start_logging(Name = CloudTrailARN)
		print("Trail created:\n Name:%s\n S3 bucket:%s\n ARN:%s" %(cloudtrail_name, S3Bucket, CloudTrailARN))

	
def main():

	account_id = ''
	aws_access_key_id = ''
	aws_secret_access_key = ''
	region_name = ''
	cloudtrail_name = ''
	enablecloudtrail(account_id, aws_access_key_id, aws_secret_access_key, region_name, cloudtrail_name) #Account ID of the root user
	

if __name__ == "__main__":
	main()