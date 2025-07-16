from functools import wraps
import concurrent.futures as con
import traceback

def try_except(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        try:
            return fn(*args,**kwargs)
        except Exception as e:
            print(e)
            traceback.print_exc()
    return wrapper

@try_except
def error_fn():
    raise TypeError('类型错误')

@try_except
def deep_error(i):
    print(f'this is layer {i}')
    if i == 1:
        try:
            with con.ProcessPoolExecutor() as pool:
                pool.submit(deep_error,i+1)
        except Exception as e:
            print(e)
    elif i < 50:
        with con.ProcessPoolExecutor() as pool:
            pool.submit(deep_error, i + 1)
        raise Exception(f'layer {i} exception!')


if __name__ == "__main__":
    deep_error(1)