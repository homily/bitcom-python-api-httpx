import httpx
import time
import hmac
from urllib import parse


class BitClient:
    _ENDPOINT = 'https://api.bit.com'           #Api_url_host
    #_ENDPOINT = 'https://betaapi.bitexch.dev'  #testnet_api

    def __init__(self,key=None, secret=None):
        self._api_key = key # TODO: Place your API key here
        self._api_secret = secret # TODO: Place your API secret here

    #鉴权参数按顺序排列
    def _pop_none(self,data):
        for k in list(data .keys()):
            if not (data[k]):
                del data [k]
        return (data)

    #构造get函数
    def _get(self, path: str, data):
        data=self._pop_none(data)
        data['timestamp']=int(time.time() * 1000)
        data['signature']=self._sign_request(path,data)
        data=self._pop_none(data)
        return self._request('GET',path,params=data)

    #构造post函数
    def _post(self, path: str, data):
        data=self._pop_none(data)
        data['timestamp']=int(time.time() * 1000)
        data['signature']=self._sign_request(path,data)
        data=self._pop_none(data)
        return self._request('POST',path,json=data)

    #构造请求
    def _request(self, method: str, path: str,**data):
        with httpx.Client() as client:
            request = client.build_request(method, self._ENDPOINT + path,**data)
            if self._api_key is not None:
                request.headers['X-Bit-Access-Key']=self._api_key
            response = client.send(request)
            return (self._process_response(response))

    #构造鉴权
    def _sign_request(self,path,data):
        data = sorted(data.items(),key = lambda x:x[0])#排序
        #print(data)
        data=path+'&'+parse.urlencode(data)     #str_to_sign = api_path + '&' + params
        if (self._api_secret!=None):
            #print(self._api_secret)
            signature=hmac.new(self._api_secret.encode(), data.encode(), 'sha256').hexdigest()
            return(signature)
        else:
            return(0)

    #异常输出
    def _process_response(self,response):
        try:
            data = response.json()

        except ValueError:
            response.raise_for_status()
            raise
        else:
            if data['code']!=0:
                raise Exception(data['code'],data['message'])
            return data['data']


    #==============================================================================
        
    #查询服务器时间戳
    def get_time(self):
        data={}
        return self._get(f'/v1/system/time',data)

    #查询账户信息
    def get_account(self,currency:str):
        data={'currency':currency}
        return self._get(f'/v1/accounts',data)

    #查询市场ticker
    def get_tickers(self,instrument_id:str):
        data={'instrument_id': instrument_id}
        return self._get(f'/v1/tickers',data)

    #下单
    def post_orders(self,instrument_id,qty,side,price,order_type):
        data={'instrument_id':instrument_id,
              'price':price,
              'qty':qty,
              'side':side,
              'order_type':order_type,
              }
        return self._post(f'/v1/orders',data)

    #查询kline
    def get_kline(self,instrument_id:str,start_time:int,end_time:int,timeframe_min:str):
        data = {
            'instrument_id': instrument_id,
            'start_time':start_time,
            'end_time':end_time,
            'timeframe_min':timeframe_min,#周期(分钟) (1, 3, 5, 15, 30, 60, 120, 240, 360, 720, 1440)
            }
        return self._get(f'/v1/klines',data)

    #查询仓位
    def get_positions(self,currency,category=None,instrument_id=None,offset=None,limit=None):
        data={
            'currency':currency,
            'category':category,
            'instrument_id':instrument_id,
            'offset':offset,
            'limit':limit,        
            }
        return self._get(f'/v1/positions',data)

    #查询市场ticker
    def get_tickers(self,instrument_id):
        data={'instrument_id': instrument_id}
        return self._get(f'/v1/tickers',data)




    #查询用户交割记录
    def get_user_deliveries(self,currency,category=None,instrument_id=None,start_time=None,end_time=None,offset=None:int,limit=None:int):
        data={
            'currency': currency,
            'category':category,
            'instrument_id':instrument_id,
            'start_time':start_time,
            'end_time':end_time,
            'offset':offset,
            'limit':limit,
            }
        return self._get(f'/v1/user/deliveries',data)


    #查询资金费率
    def get_funding_rate(self,instrument_id):
        data={
            'instrument_id':instrument_id,
            }
        return self._get(f'/v1/funding_rate',data)



    #查询资金费率历史
    def get_funding_rate_history(self,instrument_id,start_time:int,end_time:int,history_type):
        data={
            'instrument_id':instrument_id,
            'start_time':start_time,
            'end_time':end_time,
            'history_type':history_type,
        }
        return self._get(f'/v1/funding_rate_history',data)

    #获取市场结算价格信息
    def get_settlement_prices(self,currency,start_time:int,end_time:int):
        data={
            'currency':currency,
            'start_time':start_time,
            'end_time':end_time,
            }
        return self._get(f'/v1/settlement_prices',data)

    #获取市场全币种24小时成交量
    def get_total_volumes(self):
        data={}
        return self._get(f'/v1/total_volumes',data)






#'https://www.bit.com/docs/zh-cn'
#'https://api.bit.com'

'''
/v1/orders	                POST	下单	                private	    yes	read,trade
/v1/batchorders	                POST	批量下单	        private	    yes	read,trade
/v1/amend_orders	        POST	修改订单	        private	    yes	read,trade
/v1/amend_batchorders	        POST	批量改单	        private	    yes	read,trade
/v1/cancel_orders	        POST	取消订单	        private     yes	read,trade
/v1/close_positions	        POST	平仓	                private	    yes	read,trade
/v1/blocktrades	                POST	block trade下单	        private	    yes	read,block_trade
/v1/account_configs/cod 	POST	更新COD配置	        private	    yes	read,trade
/v1/update_mmp_config	        POST	更新MMP配置	        private	    yes	read,trade
/v1/reset_mmp	                POST	重置MMP状态	        private	    yes	read,trade
/v1/open_orders	                GET	查询未结订单	        private	    no	read
/v1/orders	                GET	查询订单历史	        private	    no	read
/v1/stop_orders	                GET	查询止盈止损单历史	private	    no	read
/v1/margins	                GET	查询预估保证金	        private	    no	read
/v1/user/trades	                GET	查询用户交易记录	private	    no	read
/v1/positions	                GET	查询仓位	        private	    no	read
/v1/user/deliveries	        GET	查询交割历史	        private	    no	read
/v1/user/settlements	        GET	查询结算历史	        private	    no	read
/v1/transactions	        GET	查询交易日志	        private	    no	read
/v1/accounts	                GET	查询账户信息	        private	    no	read
/v1/ws/auth	                GET	获取websocket的token	private	    no	read
/v1/blocktrades	                GET	查询当前用户的block trade  private	no	read
/v1/platform_blocktrades        GET	查询平台的block trade	private	no	read
/v1/account_configs/cod	        GET	查询COD配置	        private	no	read
/v1/mmp_state	                GET	查询MMP状态	        private	no	read
/v1/wallet/withdraw	        POST	新增提币请求	        private	no	wallet
/v1/wallet/withdraw	        GET	查询提币请求的状态	private	no	wallet
/v1/wallet/withdrawals	        GET	查询提币请求历史记录	private	no	wallet
/v1/wallet/deposits	        GET	查询充币历史记录	private	no	wallet
/v1/system/time	                GET	查询服务器时间戳	public	no	
/v1/system/version	        GET	查询API版本	        public	no	
/v1/system/cancel_only_status	GET	查询 cancel only 状态	public	no	
/v1/instruments	                GET	查询产品列表	        public	no	
/v1/market/summary	        GET	查询市场价格汇总	public	no	
/v1/tickers	                GET	查询市场ticker	        public	no	
/v1/orderbooks	                GET	查询市场深度	        public	no	
/v1/market/trades	        GET	查询市场最新交易	public	no	
/v1/klines	                GET	查询kline	        public	no	
/v1/index	                GET	查询指数价格	        public	no	
/v1/delivery_info	        GET	查询每日交割价	        public	no	
/v1/funding_rate	        GET	查询资金费率	        public	no	
/v1/funding_rate_history	GET	查询资金费率历史	public	no	
/v1/settlement_prices	        GET	获取市场结算价格信息	public	no	
/v1/total_volumes	        GET	获取市场全币种24小时成交量	public	no
'''
