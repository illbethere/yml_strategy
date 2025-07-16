import logging
import multiprocessing as mp


def run_strategy(lock, user_script: str, param: dict):
    from xtquant.qmttools import run_strategy_file

    log = configure_logger(param["log_path"], param["strategy_name"])
    param["logger"] = log

    ret = run_strategy_file(user_script, param)
    # print(ret)
    # if ret:
    #     # 提取净值数据
    #     df = ret.get_backtest_index()[['时间', '单位净值']]
    #     # 获取 C._param 中的参数n,替换单位净值
    #     n1 = param['n1']
    #     n2 = param['n2']
    #     # print(n1,n2)
    #     df.rename(columns={'单位净值': f'档位_{n1}_{n2}'}, inplace=True)
    #     return df
    # return None
    return


def configure_logger(file, strategy_name):
    logger = mp.get_logger()
    logger.setLevel(logging.INFO)

    handler = ConcurrentRotatingFileHandler(
        filename=file,
        mode="a",
        maxBytes=1024 * 1024 * 1000,
        backupCount=5,
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        f"pid:%(process)d strategy:{strategy_name}\t|%(asctime)s[%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
