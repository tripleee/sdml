import requests
import time
import logging


def fetch_post(site, post_id):
    request_key = 'X2IphbAw)by6tgOGvQkI1w(('
    filter_key = '!Su916j_llPnZTl4o7X'
    response = requests.get("https://api.stackexchange.com/2.2/questions/{0}?site={1}&key={2}&filter={3}"
                            .format(post_id, site, request_key, filter_key))
    response_json = response.json()

    if 'backoff' in response_json:
        logging.info("backoff requested; sleeping {0}".format(
            response_json['backoff']))
        #time.sleep(response['backoff'])
        time.sleep(response_json['backoff'])

    if 'items' in response_json:
        ######## TODO: somehow signal when we are out of requests
        logging.info("{0} requests remaining".format(
            response_json['quota_remaining']))
        return response_json['items'][0]
    else:
        raise Exception('no items provided in API response')
