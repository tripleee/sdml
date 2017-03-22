#!/usr/bin/env python3

import json
from collections import defaultdict


def fetch(logger=None):
    """
    Generator to set up web socket and retrieve posts.  Yield each.
    """
    import websocket, bodyfetcher
    from time import sleep
    from ssl import SSLEOFError
    
    if logger == None:
        import logging
        logger = logging

    while True:
        ws = websocket.create_connection("ws://qa.sockets.stackexchange.com/")
        ws.send("155-questions-active")

        while True:
            try:
                recv_data = ws.recv()
            except websocket.WebSocketConnectionClosedException:
                logger.info('websocket closed; sleep(5) before reconnecting')
                sleep(5)
                break
            recv_json = json.loads(recv_data)
            logger.debug('recv_json = {0!r}'.format(recv_json))
            try:
                post_data = json.loads(recv_json['data'])
            except json.decoder.JSONDecodeError as err:
                logger.warn(
                    'ws.recv() returned data without a valid "data" member: '
                    '{0!r}'.format(recv_json))
                continue
            logger.info('ID: {0} on site: {1}'.format(
                post_data['id'], post_data['siteBaseHostAddress']))
            logger.debug('post_data = {0!r}'.format(post_data))
            try:
                full_data = bodyfetcher.fetch_post(
                    post_data['siteBaseHostAddress'], post_data['id'])
            except (IndexError, SSLEOFError) as err:
                logger.warn(
                    'bodyfetcher.fetch_post({0}, {1}) failed: {2}'.format(
                        post_data['siteBaseHostAddress'], post_data['id'], err))
                continue
            # full_data lacks the site!
            full_data['site'] = post_data['siteBaseHostAddress']
            logger.debug('yield {0!r}'.format(full_data))
            yield full_data


class SillyCounter (object):
    """
    Encapsulate simple counter for logging.info() call in main loop.
    """
    def __init__ (self, logger=None):
        if logger == None:
            import logging
            self.logger = logging
        self.count = 0
        self.sitehits = defaultdict(int)

    def hits_info(self, site):
        self.count += 1
        self.sitehits[site] += 1
        self.logger.info('{0} items downloaded; total for {1}: {2}'.format(
            self.count, site, self.sitehits[site]))


def main():
    import logging
    from sys import argv

    logging.basicConfig(level=logging.DEBUG,
        format='%(module)s [%(asctime)s]: %(message)s')

    if len(argv) != 2:
        logging.error('Syntax: {0} filename.jsons'.format(argv[0]))
        exit(1)

    counter = SillyCounter()
    with open(argv[1], 'w') as output:
        try:
            for post in fetch():
                print(json.dumps(post), file=output)
                counter.hits_info(post['site'])
        except KeyboardInterrupt:
            exit(0)


if __name__ == "__main__":
    main()
