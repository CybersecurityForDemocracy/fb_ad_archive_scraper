import os
from google.cloud import storage

class GCSUploader():

    def __init__(self, bucket_name, credentials_file_path):
        self.storage_client = storage.Client.from_service_account_json(
            credentials_file_path)
        self.bucket = self.storage_client.get_bucket(bucket_name)

    def upload_file(self, source_file_name):
        """Uploads a file to the bucket."""

        destination_blob_name = os.path.basename(source_file_name)
        blob = self.bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))
