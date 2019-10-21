import os
import logging
from google.cloud import storage

class GCSUploader():

    def __init__(self, bucket_name, credentials_file_path):
        self.storage_client = storage.Client.from_service_account_json(
            credentials_file_path)
        self.bucket = self.storage_client.get_bucket(bucket_name)

    def upload_file(self, source_file_name, gcs_file_path):
        """Uploads a file to the bucket."""
        blob = self.bucket.blob(gcs_file_path)

        blob.upload_from_filename(source_file_name)

        logging.info('File {} uploaded to {}.'.format(
            source_file_name,
            gcs_file_path))
