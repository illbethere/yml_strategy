try:
    import XtTraderPyApi
    print('XtTraderPyApi 已安装')
    print('可用的属性:', dir(XtTraderPyApi))
except ImportError as e:
    print(f'XtTraderPyApi 未安装: {e}') 