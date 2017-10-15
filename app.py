import os
import json
import constatnts
from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from metric_collector import MetricCollector

if __name__ == '__main__':
    configs = os.getenv('configs')
    if configs is None:
        print('Exiting due to missing configs')
        exit()

    try:
        configs_json = json.loads(configs)
    except:
        configs_json = dict()

    tenant_id = configs_json.get('tenant', 'test')
    api_key = configs_json.get('api_key', '97f8b5d3c3939262233fb65659a3f2c2')
    query_key = configs_json.get('query_key', '5I5-SrmDxgTVir2YuvVKvjlAFz1oFZeN')

    SCHEDULER_INTERVAL = constatnts.SCHEDULER_INTERVAL  # in seconds
    executors = {
        'default': ThreadPoolExecutor()
    }

    app_scheduler = BlockingScheduler(executors=executors, timezone=utc)

    metric_collector_instance = MetricCollector(api_key, query_key, tenant_id)
    metric_collector_instance.get_metrics()
    app_scheduler.add_job(metric_collector_instance.get_metrics, 'interval', seconds=SCHEDULER_INTERVAL,
                          id='newrelic scheduler')
    app_scheduler.start()
