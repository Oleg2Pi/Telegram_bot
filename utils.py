import requests
import json
from config import keys


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Невозможно перевести валюту {base} в валюту {quote}, так это одна валюта')
        
        try:
            base_ticket = keys[base]
        except KeyError:
            raise APIException(f'Неудалось обработать валюту {base}, проверьте наличие её в списке доступных валют')
        
        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise APIException(f'Неудалось обработать валюту {quote}, проверьте наличие её в списке доступных валют')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        response = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticket}&tsyms={quote_ticket}')
        total_quote = json.loads(response.content)[keys[quote]] * amount
        return total_quote