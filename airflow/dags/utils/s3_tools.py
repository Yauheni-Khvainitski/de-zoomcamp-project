import boto3
from botocore import UNSIGNED
from botocore.config import Config
from datetime import datetime
import os


class S3Tools():

    def __init__(self, bucket):
        self.s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        self.bucket = bucket

    def get_list_of_files(self, prefix):

        list_of_files = []

        # get the paginator
        paginator = self.s3.get_paginator('list_objects_v2')

        for page in paginator.paginate(
            Bucket=self.bucket,
            Prefix=prefix,
            ):

            for key in page['Contents']:
                list_of_files.append(key['Key'])
        
        return list_of_files

    def download_files(self, list_of_files, folder_name):
        curr_path = os.getcwd()
        download_path = os.path.join(curr_path, folder_name)

        if not os.path.exists(download_path):
            os.mkdir(download_path)
            print(f'{download_path} path created')
        elif os.path.exists(download_path):
            print(f'{download_path} path already exists')

        for file in list_of_files:
            print(f'downloading ... {os.path.join(curr_path, file)}')
            self.s3.download_file(self.bucket, file, os.path.join(curr_path, file))
            print(f'Downloaded! {os.path.join(curr_path, file)}')
