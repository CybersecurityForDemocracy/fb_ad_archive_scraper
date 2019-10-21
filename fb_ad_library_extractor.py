import os
import sys
import tempfile
import logging
import fb_archive_report_downloader
import gcs_uploader

GCS_BUCKET = 'fb_archive_reports'
GCS_CREDENTIALS_FILE = 'gcs_credentials.json'
logging.basicConfig(handlers=[logging.FileHandler("ad_library_collection.log"),
                              logging.StreamHandler()],
                    format='[%(levelname)s\t%(asctime)s] %(message)s',
                    level=logging.INFO)


def download_reports(scratch_dir, country_list):
    scraper = fb_archive_report_downloader.FacebookArchiveReportDownloader(scratch_dir, "./chromedriver")
    for country in country_list:
        logging.info('Scraping for %s and storing in directory %s', country, scratch_dir)
        scraper.set_country(country)
        scraper.download_all_reports()

    scraper.quit_driver()

def upload_dir_contents_to_cloud(bucket, credentials_file, scratch_dir):
    cloud_uploader = gcs_uploader.GCSUploader(bucket, credentials_file)
    for file_name in os.listdir(scratch_dir):
        full_path = os.path.join(scratch_dir, file_name)
        cloud_uploader.upload_file(full_path)

def main(countryfile):
    scratch_dir = tempfile.mkdtemp()
    country_list = [line.rstrip('\n') for line in open(countryfile)]
    download_reports(scratch_dir, country_list)
    upload_dir_contents_to_cloud(GCS_BUCKET, GCS_CREDENTIALS_FILE, scratch_dir)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit("Usage: python3 fb_ad_library_extractor countrylist.txt")

    main(sys.argv[1])
