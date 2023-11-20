import os
import requests
from dotenv import load_dotenv

# Load Salesforce info from .env file
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

# The API name of the Zoom Call Log custom object & API version
SOBJECT_NAME = "zoom_app__Zoom_Call_Log__c"
API_VERSION = "v56.0"

# The location of the file containing a list of record IDs
FNAME = "sample.txt"


def prepare_record_ids(fname: str) -> list[str]:
    with open(fname) as f:
        next(f)  # Skip over the first line to avoid the header
        return [line.strip('\n"') for line in f]


def get_sf_access_details() -> dict[str, str]:
    url = "https://login.salesforce.com/services/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": USERNAME,
        "password": f"{PASSWORD}{SECRET_TOKEN}",
    }
    try:
        r = requests.post(url, headers=headers, data=payload)
        r.raise_for_status()
        return r.json()
    except requests.HTTPError as err:
        print(err)


def delete_records(instance_url: str, token: str, record_ids: list[str]) -> None:
    headers = {"Authorization": f"Bearer {token}"}
    for record_id in record_ids:
        url = f"{instance_url}/services/data/{API_VERSION}/sobjects/{SOBJECT_NAME}/{record_id}"
        print(f"Deleting {record_id}")
        r = requests.delete(url, headers=headers)


def main() -> None:
    record_ids = prepare_record_ids(FNAME)
    print(record_ids)
    sf_access_details = get_sf_access_details()
    delete_records(
        sf_access_details["instance_url"], sf_access_details["access_token"], record_ids
    )


if __name__ == "__main__":
    main()
