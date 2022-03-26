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

            if 'Contents' in page:
                for key in page['Contents']:
                    list_of_files.append(key['Key'])
            else:
                print(f'No objects returned for {prefix}')
        
        return list_of_files

    def download_s3_files(self, dir, prefix):

        print(f'Listing files for {prefix}')

        list_of_files = self.get_list_of_files(prefix)

        if list_of_files:

            download_path = os.path.join(dir, prefix)

            if not os.path.exists(download_path):
                os.mkdir(download_path)
                print(f'{download_path} path created')
            elif os.path.exists(download_path):
                print(f'{download_path} path already exists')

            print(f'Downloading files for {prefix}')

            for file in list_of_files:
                print(f'downloading ... {os.path.join(dir, file)}')
                self.s3.download_file(self.bucket, file, os.path.join(dir, file))
                print(f'Downloaded! {os.path.join(dir, file)}')

            print(f'Files for {prefix} successfully downloaded')
        
        else:
            print(f'No files to list for {prefix}. Seems to be no data')
