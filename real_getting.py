###########################################################################
#   Project_name:   keyargs
#   File_name:      realtime_getting
#   Creat_time:     2024/7/20   17:19
#   Author:         富视投资 
#   Description:
###########################################################################
# 新浪 http://hq.sinajs.cn/rn={int(time.time() * 1000)}&list=sh600848,sh603172
# 东财 https://48.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112402508937289440778_1658838703304&pn=1&pz=2000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1658838703305
# https://mp.weixin.qq.com/s?__biz=MzIxNjM4NDE2MA==&mid=2247519448&idx=2&sn=dfe54ff840e8dab0d01b1d092483efef&chksm=978b1b17a0fc92018b96f0f339879ccdfb22b9086b73c3603a2b6db267547a58f00099b02596&scene=27
def get_real():
    pass


if __name__ == '__main__':
    print(__file__)


"""
https://61.push2.eastmoney.com/api/qt/stock/sse?fields=f58,f734,f107,f57,f43,f59,f169,f301,f60,f170,f152,f177,f111,f46,f44,f45,f47,f260,f48,f261,f279,f277,f278,f288,f19,f17,f531,f15,f13,f11,f20,f18,f16,f14,f12,f39,f37,f35,f33,f31,f40,f38,f36,f34,f32,f211,f212,f213,f214,f215,f210,f209,f208,f207,f206,f161,f49,f171,f50,f86,f84,f85,f168,f108,f116,f167,f164,f162,f163,f92,f71,f117,f292,f51,f52,f191,f192,f262,f294,f295,f269,f270,f256,f257,f285,f286,f748,f747&mpi=1000&invt=2&fltt=1&secid=0.300799&ut=fa5fd1943c7b386f172d6893dbfba10b&dect=1&wbp2u=|0|0|0|web
https://61.push2.eastmoney.com/api/qt/stock/details/sse?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55&mpi=1000&dect=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&pos=-11&secid=0.300799&wbp2u=|0|0|0|web
https://23.push2.eastmoney.com/api/qt/stock/details/sse?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55&mpi=1000&dect=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&pos=-11&secid=0.834407&wbp2u=|0|0|0|web

"""