import os
import tempfile
import logging
import fb_archive_report_downloader
import gcs_uploader

GCS_BUCKET = 'fb_archive_reports'
GCS_CREDENTIALS_FILE = 'gcs_credentials.json'
logging.basicConfig(handlers=[logging.FileHandler("canada_fb_api_collection.log"),
                              logging.StreamHandler()],
                    format='[%(levelname)s\t%(asctime)s] %(message)s',
                    level=logging.INFO)


def download_reports(scratch_dir, country):
    scraper = fb_archive_report_downloader.FacebookArchiveReportDownloader(scratch_dir)
    scraper.set_country(country)
    scraper.download_all_reports()
    scraper.quit_driver()

def upload_dir_contents_to_cloud(bucket, credentials_file, scratch_dir):
    cloud_uploader = gcs_uploader.GCSUploader(bucket, credentials_file)
    for file_name in os.listdir(scratch_dir):
        full_path = os.path.join(scratch_dir, file_name)
        cloud_uploader.upload_file(full_path)

def main():
    scratch_dir = tempfile.mkdtemp()
    country = 'Canada'
    logging.info('Scraping for %s and storing in directory %s', country, scratch_dir)
    download_reports(scratch_dir, country)
    upload_dir_contents_to_cloud(GCS_BUCKET, GCS_CREDENTIALS_FILE, scratch_dir)


if __name__ == '__main__':
    main()