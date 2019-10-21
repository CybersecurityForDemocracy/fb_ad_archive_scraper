# Report Collector
This is a system to simply download all presently available Facebook ad archive reports and
store them in a given GCS buket.

## How to use this tool

Please add your GCS credentials to the repo root as `gcs_credentials.json`

Then create a virtual environment with:

```
virtualenv venv -p python3
```

Then activate the environment and install the required deps:

```
source venv/bin/activate
pip install -r requirements.txt
```


Assuming everything is now setup correctly, use the following command to upload data to your GCS bucket:


```
python fb_ad_library_extractor.py
```