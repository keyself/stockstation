###########################################################################
#   Project_name:   keyargs
#   File_name:      get_history
#   Creat_time:     2024/7/21   0:02
#   Author:         富视投资 
#   Description:
###########################################################################
from stockstation import get_history

if __name__ == '__main__':
    # get_history()
    # get_history(symbols='600848, 600252')
    # get_history(symbols='600848')
    historyDict = get_history(symbols='600848, 000520', period='d', start='20010205', end='20241102')
    print(historyDict)
