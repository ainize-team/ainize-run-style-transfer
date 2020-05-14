import requests

def track_event(category, action, label=None, value=0):
  data = {
    'v': '1',
    'tid': 'UA-164242824-5',
    'cid': '555',
    't': 'event',
    'ec': category,
    'ea': action,
    'el': label,
    'ev': value,
    'ua': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
  }

  response = requests.post(
    'https://www.google-analytics.com/collect', data=data)

  response.raise_for_status()
