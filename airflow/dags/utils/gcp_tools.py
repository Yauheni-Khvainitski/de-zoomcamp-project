import os
from google.cloud import storage

class GCPTools():

    def __init__(self, gcs_prefix):
        self.PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
        self.BUCKET = os.environ.get("GCP_GCS_BUCKET")
        self.STORAGE_CLIENT = storage.Client()
        self.gcs_prefix = gcs_prefix


    def upload_to_gcs(self, local_dir, prefix):

        try:
            list_of_files = os.listdir(os.path.join(local_dir, prefix))

            bucket = self.STORAGE_CLIENT.bucket(self.BUCKET)

            for file in list_of_files:
                print(f"Uploading {file} to GCS ...")
                gcs_obj_name = os.path.join(self.gcs_prefix, prefix, file)
                blob = bucket.blob(gcs_obj_name)
                blob.upload_from_filename(os.path.join(local_dir, prefix, file))
                print(f"{file} successfully uploaded to GCS")
        except FileNotFoundError:
            print(f"Seems to be no files for {prefix}")
        except:
            raise
