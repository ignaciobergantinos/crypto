from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=100&sort=market_cap&cryptocurrency_type=all&tag=all'
parameters = {

}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '70af2400-4214-4859-8223-40fa3f029dc2',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

  # https://coinmarketcap.com/currencies/qatar-2022-token/


