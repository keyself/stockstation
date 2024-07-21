###########################################################################
#   Project_name:   keyargs
#   File_name:      common
#   Creat_time:     2024/7/20   22:05
#   Author:         富视投资 
#   Description:
###########################################################################
import copy
import inspect
import os
import time

import pandas as pd


def get_function_name(level=1):
    """当前函数名 返回函数名
    注意：返回的是 str，不是对象
    """
    caller = inspect.stack()[level]
    return caller.function


def get_function_parameters(func):
    """函数的所有参数
    如果是位置参数就用元组 如果是关键字参数就用字典
    注意：形参func必须是对象，不能是str，也不能在这里eval(func)
    """
    # 所有参数组成的字典
    signature = inspect.signature(func)

    # 返回 (...), {...}
    return tuple([param.name for param in signature.parameters.values() if param.default is inspect._empty]), \
        {param.name: param.default for param in signature.parameters.values() if param.default is not inspect._empty}


def symbols_to_list(symbols):
    """检查股票代码格式，转为list"""
    if isinstance(symbols, str):
        symbols = symbols.replace(' ', '').split(',')
    elif isinstance(symbols, tuple):
        symbols = list(symbols)
    elif isinstance(symbols, list):
        pass
    else:
        raise TypeError("股票代码只接受 str tuple list")

    return symbols


def find_same_content_symbols(folder_path):
    """股票历史数据是否有重复"""
    dic = dict()
    # 要检查的文件夹
    gen = os.walk(folder_path)
    for root, folder, filenames in gen:
        for filename in filenames:
            # 读入所有数据
            file = os.path.join(root, filename)
            # print(file)
            df = pd.read_csv(file)
            # print(filename[:6])
            if len(df) > 1:
                dic.update({filename[:6]: df.iloc[1].to_list()})

    same_list = list()
    # 新字典 去掉当前项的    # 剩下的
    newdict = copy.deepcopy(dic)
    for symbol, value in dic.items():  # 要比较的一个
        newdict.pop(symbol)
        # 如果当前项的值在新字典里能找到,说明是有重复的
        for k, v in newdict.items():
            if value == v:
                same_list.append(symbol)
                same_list.append(k)
    # 集合可以去重
    s = set(same_list)
    same_list = list(s)

    return same_list


def market(symbol):
    """
    获取股票代码市场前缀
    （获取股票代码对应的证券市场，sh、sz）
    """
    # 断言
    assert type(symbol) is str, "symbol need str type"

    if symbol.startswith(('sh', 'sz', 'SH', 'SZ')):
        return symbol[:2]

    sh_head = ("50", "51", "60", "90", "110", "113", "118",
               "132", "204", "5", "6", "9", "7")

    return 'sh' if symbol.startswith(sh_head) else 'sz'


def check_symbols(symbols):
    """检查股票代码格式，转为list"""
    if isinstance(symbols, str):
        symbols = symbols.replace(' ', '').split(',')
    elif isinstance(symbols, tuple):
        symbols = list(symbols)
    elif isinstance(symbols, list):
        pass
    else:
        raise TypeError("股票代码只接受 str tuple list")

    return symbols


# 函数装饰器 计算函数运行时间
def runtime(fn):
    def inner(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        print(f"下载 {len(result.keys())} 只股票历史k线数据, 用时: {time.time() - start}")
        return result

    return inner
