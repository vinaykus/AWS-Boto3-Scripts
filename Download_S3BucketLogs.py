# -*- coding: utf-8 -*-

'''

Author      : Shalini Sasidharan
Description : This script will download all the logs till the previous date from the specified
              S3 Bucket to the server, retaining the original folder structure of the S3 Bucket.

INPUT PARAMETERS:

	aws_access_key_id           ** Required
    aws_secret_access_key       ** Required
    region_name                 ** Required
	S3Bucket                    ** Required

'''

import boto3
import random
import json
import botocore
from boto.s3.key import Key
import os
import gzip
import datetime


def download_logs(aws_access_key_id, aws_secret_access_key, region_name, S3Bucket):

	session = boto3.Session(region_name=region_name,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
	
	s3client = session.client('s3')

	all_objects = s3client.list_objects(Bucket=S3Bucket)['Contents']
	

	for obj in all_objects:
		Key = obj['Key']
		LastModified = obj['LastModified'] #LastModified Time is in GMT format
    
		#downloads only the logs untill the previous date
		if LastModified.strftime("%Y-%m-%d")  < datetime.datetime.utcnow().strftime("%Y-%m-%d"):
    
			path_name = Key[:Key.rfind('/')+1]
			
			#for each key, a directory structure is created if not exists already
			if not os.path.exists(path_name):
				os.makedirs(path_name)
			
			if Key.endswith( ('.json.gz')): 
				s3client.download_file(S3Bucket, Key, Key)       
				
def main():
	download_logs(<aws_access_key_id>, <aws_secret_access_key>, <region_name>, <S3Bucket>) 
	

if __name__ == "__main__":
	main()
				