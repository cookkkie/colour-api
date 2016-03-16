# Colour-api
## Description

A very simple lib to get colors from http://www.colourlovers.com

## How-to

First, install all the requirements : `pip install -r requirements.txt`.

To retrieve colors you should first instanciate an api object.

```python
from color_api import Api

api = Api()
```

You can pass a aiohttp.ClientSession `session` object paramater and an asyncio
event loop `loop` parameter.

Then you just await from `api.find`.

```python
colors = await api.find('your_color_name')
```

Colors is a list of `color.Color` objects.

Enjoy ;) .
