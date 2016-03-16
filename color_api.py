import asyncio
import aiohttp
from bs4 import BeautifulSoup
from color import Color
import errors

class Api(object):
    """Represents the colour API.

    You should pass an event loop !

    Parameters
    ----------
    loop : Optional[event loop]
        An asyncio event loop.
        If None, asyncio.get_event_loop() will be used.
    session : Optional[aiohttp.ClientSession]
        An aiohttp session

    Attributes
    ----------
    website_url : str
        The website url.
    """
    def __init__(self, **kwargs):
        self.loop = kwargs.get('loop', asyncio.get_event_loop())
        self.session = kwargs.get('session', aiohttp.ClientSession(loop=self.loop))
        self.website_url = "http://www.colourlovers.com"

    @asyncio.coroutine
    def _get_page(self, url, params={}):
        query = yield from self.session.get(url, params=params)

        if query.status!=200:
            raise errors.QueryProblem

        page = yield from query.text()
        return page

    @asyncio.coroutine
    def find(self, color_name):
        url = "{}/ajax/search-colors/".format(self.website_url)
        params = {'query': color_name, 'sortCol': 'votes', 'sortBy':'desc'}
        page = yield from self._get_page(url, params)

        colors = self.extract_colors(page)
        return colors

    def extract_colors(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        divs = soup.find_all('div', class_='detail-row')
        colors = []

        for div in divs:
            name = div.find('h3').text
            h4s = div.find_all('h4')
            rgb = tuple(map(int, h4s[1].text.split(',')))
            hex_code = h4s[0].text

            colors.append(Color(name, rgb, hex_code))

        return colors
