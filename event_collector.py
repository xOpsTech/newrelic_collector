import requests
import hashlib
import constatnts
from elasticsearch import Elasticsearch

es = Elasticsearch(constatnts.ES_IP)


# URL = "https://synthetics.newrelic.com/synthetics/api/v3/monitors"


class EventCollector(object):
    def __init__(self, api_key, tenant_id):
        self.api_key = api_key
        self.tenant_id = tenant_id
        self.header = {'Accept': 'application/json', 'X-Api-Key': api_key}

    def get_violations(self):
        response = requests.get(constatnts.ALERT_VIOLATION_URL, headers=self.header, verify=False)
        htttp_response_code = response.status_code if response is not None else 'response_null'
        if htttp_response_code != 200:
            raise Exception('response error', htttp_response_code)
        data = response.json()
        return data

    def get_alerts(self):
        violations = self.get_violations()