import requests
import urllib.parse
import constatnts


QUERY = "SELECT *  from SyntheticCheck where monitorId in ({TEST_ID_LIST}) since {DURATION} minutes ago LIMIT 1000"
NEWRELIC_QUERY_DURATION = 10


class InsightDB(object):
    def __init__(self, api_key):
        self.header = {'Accept': 'application/json', 'X-Query-Key': '5I5-SrmDxgTVir2YuvVKvjlAFz1oFZeN'}

    def get_test_result(self, test_ids):
        if test_ids:
            query = QUERY.format(TEST_ID_LIST=test_ids,
                                 DURATION=NEWRELIC_QUERY_DURATION if NEWRELIC_QUERY_DURATION else 40)
            try:
                result = self._query_insight(query)
                return result
            except Exception as e:
                print('process: get newrelic test result | status: unsuccessful | reason: ', e)
        else:
            print('process: get newrelic test result | status: unsuccessful | reason: %s',
                  'test_id cannot be NULL')

    def _query_insight(self, query):
        encoded_query = urllib.parse.quote_plus(query)
        response = requests.get(constatnts.INSIGHT_URL + encoded_query, headers=self.header, verify=False)
        htttp_response_code = response.status_code if response is not None else 'response_null'
        if htttp_response_code != 200:
            raise Exception('response error', htttp_response_code)
        data = response.json()
        return data['results'][0]["events"]
