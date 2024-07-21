###########################################################################
#   Project_name:   keyargs
#   File_name:      easthistory
#   Creat_time:     2024/7/21   0:18
#   Author:         富视投资 
#   Description:
###########################################################################
import datetime
import json
import time

import pandas as pd
from jsonpath import jsonpath

from stockstation.base_history import HistoryBase
from stockstation.common import market

# f2 最新价f3 涨跌幅f4 涨跌额f5 总手f6 成交额f7 振幅f8 换手率f9 市盈率f10 量比f11 5分钟
# 涨跌幅f12 股票代码f13 市场f14 股票名称f15 最高价f16 最低价f17 开盘价f18 昨收f20 总
# 市值f21 流通市值f22 涨速f23 市净率f24 60日涨跌幅f25 年初至今涨跌幅f26 上市日期f28
# 昨日结算价f30 现手f31 买入价f32 卖出价f33 委比f34 外盘f35 内盘f36 人均持股数f37 净
# 资产收益率(加权)f38 总股本f39 流通股f40 营业收入f41 营业收入同比f42 营业利润f43 投
# 资收益f44 利润总额f45 净利润f46 净利润同比f47 未分配利润f48 每股未分配利润f49 毛利
# 率f50 总资产f51 流动资产f52 固定资产f53 无形资产f54 总负债f55 流动负债f56 长期负债
# f57 资产负债比率f58 股东权益f59 股东权益比f60 公积金f61 每股公积金f62 主力净流入
# f63 集合竞价f64 超大单流入f65 超大单流出f66 超大单净额f69 超大单净占比f70 大单流入
# f71 大单流出f72 大单净额f75 大单净占比f76 中单流入f77 中单流出f78 中单净额f81 中单
# 净占比f82 小单流入f83 小单流出f84 小单净额f87 小单净占比f88 当日DDXf89 当日
# DDYf90 当日DDZf91 5日DDXf92 5日DDYf94 10日DDXf95 10日DDYf97 DDX飘红天数
# (连续)f98 DDX飘红天数(5日)f99 DDX飘红天数(10日)f100 行业f101 板块领涨股f102 地区
# 板块f103 备注f104 上涨家数f105 下跌家数f106 平家家数f112 每股收益f113 每股净资产
# f114 市盈率（静）f115 市盈率（TTM）f124 当前交易时间f128 板块领涨股f129 净利润
# f130 市销率TTMf131 市现率TTMf132 总营业收入TTMf133 股息率f134 行业板块的成分
# 股数f135 净资产f138 净利润TTMf221 更新日期f400 pre：盘前时间after：盘后时间
# period：盘中时间


class EastHistory(HistoryBase):
    """东财 历史数据采集类 ：抽象基类的具体实现类
    注意:
        self._symbols是原始股票代码
        self.symbols是个性化股票代码

        指定请求头可以直接用self.url,self.headers而不必使用self._url
        请求url和请求头会自动更新，而不是新值

        从父类继承属性 self.args, self.kwargs, self.symbols等
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?'
        self.headers = {
            "Host": "push2his.eastmoney.com",
            'Referer': 'http://quote.eastmoney.com/'
        }

    def format_symbols(self):
        """个性化所有的股票代码"""
        return ["0." + symbol[-6:] if market(symbol) == "sz" else "1." + symbol[-6:] for symbol in
                self._symbols][:]

    def format_parameters(self, symbol) -> dict:
        """个性化处理请求参数"""
        # 发起请求前构造参数 批处理因子 和 参数的组合
        params = {
            'fields1': 'f2',
            # 'fields2': 'f51,f52,f53,f54,f55,f56,f61',
            'ut': '7eea3edcaed734bea9cbfc24409ed989',
            '_': str(time.time()),
        }

        # k线周期
        # 对应关系
        pattern = {'d': '101',
                   'w': '102',
                   'm': '103',
                   's': '104',
                   'b': '105',
                   'y': '106',
                   '5': '5',
                   '15': '15',
                   '30': '30',
                   '60': '60',
                   }
        # 把传进来的参数转换为个性化的请求参数
        # 如 传进来的period='d'， 对应 klt=101
        params['klt'] = pattern[self.kwargs.get('period', 'd')]

        # 起止日期
        params['beg'] = self.kwargs.get('start', '0')
        if params['beg'] is None:
            params['beg'] = '0'

        end = self.kwargs.get('end', None)
        if end is None:
            today = datetime.date.today()
            end = datetime.datetime.strftime(today, '%Y%m%d')
        params['end'] = end

        # 股票代码
        params['secid'] = symbol

        # 是否复权
        adjust = self.kwargs.get('adjust', '-1')
        if adjust is None:
            params['fqt'] = '1'
        elif adjust == '0':
            params['fqt'] = '0'
        elif adjust == '-1':
            params['fqt'] = '1'     # 前复权
        elif adjust == '1':
            params['fqt'] = '2'
        else:
            params['fqt'] = '1'

        # 要爬取的字段
        fileds_pattern = {'datetime': 'f51',
                          'open': 'f52',
                          'close': 'f53',
                          'high': 'f54',
                          'low': 'f55',
                          'volume': 'f56',
                          'turnover': 'f61',
                          'unknown': 'f57',
                          }
        params['fields2'] = ','.join([fileds_pattern[field] for field in self._fields])
        # params['fields2'] = ','.join([value for key, value in fileds_pattern.items()])

        return params

    def process_single_response(self, symbol, raw_response) -> dict:
        """加工 单次请求得到的结果 """
        json_response = json.loads(raw_response)

        klines = jsonpath(json_response, "$..klines")

        if not klines or klines is None:
            return None

        klines = klines[0]
        # 统一转换为 df 格式
        line = [bar.split(',') for bar in klines]

        # fields = self.kwargs.get('fields', None)
        # if fields:
        #     fields = check_symbols(fields)
        #     if len(fields) < 7:
        #         fields = "datetime, open, close, high, low, volume, turnover".split(',')
        # else:
        #     fields = "datetime, open, close, high, low, volume, turnover".split(',')

        df = pd.DataFrame(
            data=line,
            columns=self._fields
        )

        # 设置索引
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)


        # fields = self.kwargs.get('fields', None)
        # if fields:
        #     fields = check_symbols(fields)
        # else:
        #     fields = "datetime, open, close, high, low, volume, turnover".replace(' ', '').split(',')
        # print(df.keys())
        return {symbol[-6:]: df}
