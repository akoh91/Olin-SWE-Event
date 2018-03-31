import requests


def get_uaa_token(url, b64_client_credentials):
    """
    How to get a Predix UAA token through client credentials
    Access token is a temporary pass to get information from authorized services such as timeseries
    """

    full_uaa_url = uaa_url + '/oauth/token'

    uaa_headers = {'Authorization': 'Basic ' + b64_client_credentials, 'Content-Type': 'application/x-www-form-urlencoded'}
    uaa_data = 'grant_type=client_credentials'

    uaa_response = requests.post(full_uaa_url, headers=uaa_headers, data=uaa_data)

    if uaa_response.status_code != 200:
        print "UAA call failed with code: ", uaa_response.status_code
        raise Exception("Unable to get token. Please check your UAA url or credentials.")

    # This is your access token
    access_token = uaa_response.json().get('access_token')

    return access_token


def get_timeseries_data(url, zone_id, uaa_token, start, end, tags):
    """
    How to get Predix Timeseries data
    An access_token is required to query for data
    """

    zone_id_header = 'Predix-Zone-Id'

    ts_headers = {'Authorization': 'Bearer ' + uaa_token, zone_id_header: zone_id, 'Content-Type': 'application/json'}

    ts_data = {"start": start, "end": end, "tags": [{"name": tags}]}

    ts_response = requests.post(url, headers=ts_headers, data=str(ts_data))
    if ts_response.status_code != 200:
        print "Timeseries call failed with code: ", ts_response.status_code
        raise Exception("Unable to get timeseries data. Check your timeseries information!")

    return ts_response.json()


# To access Cloud Foundry (CF) environment variables, run 'cf e <your_app_name>'

# Copy the uri value from the predix-uaa section of your CF env variables
# Should end in predix-uaa.run.aws-usw02-pr.ice.predix.io
uaa_url = ''

# Copy base64ClientCredential value from your CF env variables
base64_client_credential = ''
token = get_uaa_token(uaa_url, base64_client_credential)
print token

# Copy the uri value from the query section of the predix-timeseries section of your CF env variables
# Should begin with https and end with run.aws-usw02-pr.ice.predix.io/v1/datapoints
ts_url = ''

# Copy the zone-http-header-value value from the query section of the predix-timeseries section of your CF env variables
ts_zone_id = ''

# Query start in epoch millis
start_time_millis = 0
# Query end in epoch millis
end_time_millis = 0
# List of tags to query for (list of strings)
# Tags will be <NUC-Hostname>:<sensor> where NUC-hostname starts with WR-IDP
ts_tags = []

ts_response_data = get_timeseries_data(ts_url, ts_zone_id, token, start_time_millis, end_time_millis, ts_tags)
# print ts_response_data

# Example of how to parse data
first_tag = ts_response_data.get('tags')[0]
first_tag_name = first_tag.get('name')
first_tag_data = first_tag.get('results')[0].get('values')
# [timestamp, value, quality]
first_tag_first_data_point = first_tag_data[0]

print first_tag_name
# print first_tag_data
print first_tag_first_data_point
