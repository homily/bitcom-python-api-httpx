# bit.com
bit.com SDK （HTTPX）
bit.com交易所SDK


```
from bit import *
from pprint import pp


Access_Key='YOU ak'
Secret_Key='YOU sk'

x=BitClient(Access_Key,Secret_Key)


pp(x.get_time())
pp(x.get_account('BTC'))
pp(x.get_positions('BTC','future'))
pp(x.get_tickers('ETH-PERPETUAL'))
pp(x.get_kline('ETH-PERPETUAL',1614821270695,1614827271695,'15'))


pp(x.get_funding_rate('ETH-PERPETUAL'))
pp(x.get_total_volumes())
pp(x.get_funding_rate_history('ETH-PERPETUAL',1614721270695,1614827271695,'24H'))
pp(x.get_settlement_prices('BTC',1614721270695,1614827271695))
```







#s=x.post_orders('BTC-PERPETUAL','20','buy','48000.0','limit')
