###########################################################################
#   Project_name:   keyargs
#   File_name:      history_getting
#   Creat_time:     2024/7/20   17:16
#   Author:         富视投资 
#   Description:
###########################################################################
import json
import os

from stockstation.common import get_function_parameters, get_function_name, check_symbols
from stockstation.config import DATASFOLDER
from stockstation.eastmoney.easthistory import EastHistory


def get_history(symbols=None,
                period='d',
                start=None,
                end=None,
                fields="datetime,open,close,high,low,volume,turnover",
                adjust='-1',
                spider: object = None,
                update=True,
                path=DATASFOLDER,
                savetype='csv'
                ):
    """
    获取股票历史数据
    :param symbols:     股票代码    支持str,list、tuple格式，多个以,分隔    None为全市场
    :param period:      k线周期，   str格式，d日 m月 w周 s季 y年 5分钟
    :param start:       开始日期    str格式，'20010203'                    None为最早日期
    :param end:         结束日期    str格式，'20240511'                    None为今天
    :param fields:      k线字段    str格式，默认包含7条
    :param adjust:      复权       str格式，-1前、0不、1后              默认前复权 -1
    :param spider:        来源网站    数据采集类 对象
    :param update:      是否从网上更新     默认是
    :param path:        如果update为False path为本地读取路径 如果update为True path为本地存储路径
    :param savetype:  存储的文件类型 默认是csv
    :return:   字典
                    {'600847':
                            [
                                ['20010203', 5.62, 5.88, 5.99, 5.55, 123456, 9.9],
                                ['20010203', 5.62, 5.88, 5.99, 5.55, 123456, 9.9],
                                ['20010203', 5.62, 5.88, 5.99, 5.55, 123456, 9.9]
                            ],
                    '000520':
                            [
                                ['20010203', 5.62, 5.88, 5.99, 5.55, 123456, 9.9],
                                ['20010203', 5.62, 5.88, 5.99, 5.55, 123456, 9.9],
                                ['20010203', 5.62, 5.88, 5.99, 5.55, 123456, 9.9]
                            ],
                    ... ...
                    }
    """

    # 整理股票代码
    if symbols is None:
        with open(os.path.join(DATASFOLDER, 'stocks.json'), 'r') as f:
            symbols = json.load(f)['stocks'][:]
    # 原始股票代码
    symbols = check_symbols(symbols)

    # 参数打包以方便传值
    # 本函数的所有形参
    args, kwargs = get_function_parameters(eval(get_function_name()))
    # 把实参赋值给形参
    for key, value in kwargs.items():
        kwargs[key] = eval(key)

    # 默认指定从网上下载
    if update:
        return update_history(*args, **kwargs)

    # 本地读取
    return load_history(*args, **kwargs)


def load_history(*args, **kwargs):
    print(kwargs)


def update_history(*args, **kwargs):
    """
    从网上下载历史交易数据
    """
    # 实例化采集类
    spiderClass = kwargs.get('spider') or EastHistory  # 是否已指定采集类
    spider = spiderClass(*args, **kwargs)

    # 调用采集类的update方法进行采集
    historyDict = spider.update()

    return historyDict


if __name__ == '__main__':
    get_history()
