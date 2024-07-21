###########################################################################
#   Project_name:   keyargs
#   File_name:      __init__.py
#   Creat_time:     2024/7/20   17:15
#   Author:         富视投资 
#   Description:    数据集散中心：采集和存储股票数据
###########################################################################

# 对外接口

# 获取历史交易数据
from .history_getting import get_history

# 获取实时行情
from .real_getting import get_real

