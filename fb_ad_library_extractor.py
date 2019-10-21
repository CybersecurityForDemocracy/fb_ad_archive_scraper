import sys
import os
import sys
import tempfile
import logging
import fb_archive_report_downloader
import gcs_uploader
from slack_notifier import notify_slack
import traceback
import io
GCS_BUCKET = 'fb_archive_reports'
GCS_CREDENTIALS_FILE = 'gcs_credentials.json'
logging.basicConfig(handlers=[logging.FileHandler("ad_library_report_collection.log"),
                              logging.StreamHandler()],
                    format='[%(levelname)s\t%(asctime)s] {%(pathname)s:%(lineno)d} %(message)s',
                    level=logging.INFO)


def download_reports(scratch_dir, country):
    scraper = fb_archive_report_downloader.FacebookArchiveReportDownloader(scratch_dir, "./chromedriver")
    scraper.download_all_reports(country)
    scraper.quit_driver()

def upload_country_contents_to_cloud(country, scratch_dir, bucket, credentials_file):
    cloud_uploader = gcs_uploader.GCSUploader(bucket, credentials_file)
    for file_name in os.listdir(scratch_dir):
        file_path = os.path.join(scratch_dir, file_name)
        upload_path = os.path.join(country, file_name)
        logging.info("saving {0} for {1} at {2}".format(file_name, country, upload_path))
        cloud_uploader.upload_file(file_path, upload_path)

def main(countryfile):
    scratch_dir = tempfile.mkdtemp()
    country_list = [line.rstrip('\n') for line in open(countryfile)]
    try:
        for country in country_list:
            scratch_dir = tempfile.mkdtemp()
            logging.info('Scraping for %s and storing in directory %s', country, scratch_dir)
            download_reports(scratch_dir, country)
            upload_country_contents_to_cloud(country, scratch_dir, GCS_BUCKET, GCS_CREDENTIALS_FILE)
    except (Exception, RuntimeError) as e:
        trace = io.StringIO()
        traceback.print_exc(file=trace)

        logging.error(trace.getvalue())
        # notify_slack(str(trace.getvalue()))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit("Usage: python3 fb_ad_library_extractor countrylist.txt")

    main(sys.argv[1])
