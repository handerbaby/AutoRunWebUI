import os

# 根目录
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(dir)

# 基类目录
BASEDIR = os.path.join(dir, 'base')
# print(BASEDIR)

# 基类工厂目录
FACTORYDIR = os.path.join(BASEDIR, 'factory')
# print(FACTORYDIR)

# 存放数据目录
DATADIR = os.path.join(dir, 'data')
# print(DATADIR)

# 配置类目录
CONFIGDIR = os.path.join(dir, 'config')
# print(CONFIGDIR)

# 测试结果存放目录
RESULTDIR = os.path.join(dir, 'result')
# print(RESULTDIR)

# 日志存放目录
LOGDIR = os.path.join(RESULTDIR, 'log')
# print(LOGDIR)

# 测试报告存放目录
REPORTDIR = os.path.join(RESULTDIR, 'report')
# print(REPORTDIR)

# 测试截图存放目录
SCREENSHOTDIR = os.path.join(RESULTDIR, 'screenshot')
# print(SCREENSHOTDIR)

# 测试用例存放目录
CASEDIR = os.path.join(dir, 'case')
# print(CASEDIR)