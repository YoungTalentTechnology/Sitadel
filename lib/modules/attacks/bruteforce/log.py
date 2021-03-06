from urllib.parse import urljoin

from lib.utils.container import Services
from .. import AttackPlugin


class Log(AttackPlugin):

    def process(self, start_url, crawled_urls):
        output = Services.get('output')
        datastore = Services.get('datastore')
        request = Services.get('request_factory')

        output.info('Checking common log files..')
        with datastore.open('log.txt', 'rb') as db:
            dbfiles = [x.strip() for x in db]
            try:
                for d in dbfiles:
                    url = urljoin(start_url, d[0])
                    resp = request.send(
                        url=url,
                        method="GET",
                        payload=None,
                        headers=None
                    )
                    if resp.status_code == 200:
                        if resp.url == url.replace(' ', '%20'):
                            output.finding('Found log file at %s' % (resp.url))
            except Exception as e:
                print(e)
