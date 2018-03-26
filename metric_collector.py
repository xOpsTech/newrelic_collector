import requests
from insight_db import InsightDB
import urllib3
import hashlib
import constatnts
from locations import locations
from elasticsearch import Elasticsearch

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
es = Elasticsearch(constatnts.ES_IP)


# URL = "https://synthetics.newrelic.com/synthetics/api/v3/monitors"


class MetricCollector(object):
    def __init__(self, api_key, query_key, tenant_id):
        self.api_key = api_key
        self.query_key = query_key
        self.tenant_id = tenant_id
        self.header = {'Accept': 'application/json', 'X-Api-Key': api_key}
        self.insightDb = InsightDB(api_key)

    def get_monitors(self):
        response = requests.get(constatnts.MONITOR_URL, headers=self.header, verify=False)
        htttp_response_code = response.status_code if response is not None else 'response_null'
        if htttp_response_code != 200:
            raise Exception('response error', htttp_response_code)
        data = response.json()
        return data

    def get_monitor_ids(self):
        monitor_id_list = list()
        try:
            monitors = self.get_monitors()['monitors']
            for monitor in monitors:
                monitor_id = monitor['id']
                monitor_id_list.append(monitor_id)

            return monitor_id_list
        except Exception as e:
            print('process: get newrelic monitors | status: unsuccessful | reason: ', e)

    def get_metrics(self):
        monitor_id_list = self.get_monitor_ids()
        if monitor_id_list:
            test_ids = ','.join(["'%s'" % testId for testId in monitor_id_list])
            newrelic_result_list = self.insightDb.get_test_result(test_ids)

            for newrelic_result in newrelic_result_list:
                write_to_es(newrelic_result, self.tenant_id)


def write_to_es(newrelic_metric, tenant):
    try:
        es_index = 'metrics-' + tenant
        es_doc_type = 'newrelic-synthetics'
        es_doc_id = get_id(newrelic_metric)
        newrelic_metric['value'] = newrelic_metric.get('duration')
        enrich_with_location_coordinates(newrelic_metric)
        es.index(id=es_doc_id, index=es_index, doc_type=es_doc_type, body=newrelic_metric)
        print('process: write to es | id: %s | index: %s | status: successful' % (es_doc_id, es_index))
    except Exception as e:
        print('process: write to es | id: %s | index: %s | newrelic_metric: %s | status: unsuccessful | reason: %s' % (
            es_doc_id, es_index, newrelic_metric, e))


def get_id(newrelic_metric):
    str_to_hash = '%s%s%s' % (
        newrelic_metric['monitorId'], newrelic_metric['location'], newrelic_metric['timestamp'])
    return hashlib.md5(str(str_to_hash).encode('utf-8')).hexdigest()


def enrich_with_location_coordinates(newrelic_metric):
    newrelic_metric['locationCoordinates'] = locations.get(newrelic_metric['locationLabel'], '0,0')
