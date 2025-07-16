import datetime
import pandas as pd
from datetime import datetime, time


class StrategyManager:
    def __init__(self, order_manager):
        self.order_manager = order_manager

    def strategy_1(self, code: str, start_time: str, end_time: str, raw_data: pd.DataFrame, k1: float, k2: float, lot: int, slip: float) -> pd.DataFrame:
        #k1:开仓信号，k2:平仓信号
        #manager = order_manager()
        start_time = datetime.strptime(start_time, '%Y%m%d')
        end_time = datetime.strptime(end_time, '%Y%m%d')

        data = raw_data.loc[start_time:end_time].copy()
        basis_org = data['basis'].iloc[0]

        time_list = list(data.index)
        for time_now in time_list:
            basis = data.loc[time_now]['basis']
            b_signal = basis - basis_org
            #print(f"当前时间: {time_now}, 类型: {type(time_now)}")
            #注意list(manager.open_orders.items())返回的是许多元组构成的列表，每个元组为（id,字典）
            for order_id, order_info in list(self.order_manager.open_orders.items()):

                if order_info['position'] == 1 and b_signal <= k2:
                    self.order_manager.close_order(
                        order_id=order_id,
                        price=data.loc[time_now]['contract_close'],
                        close_time=time_now
                    )
                elif order_info['position'] == -1 and b_signal >= -k2:
                    self.order_manager.close_order(
                        order_id=order_id,
                        price=data.loc[time_now]['contract_close'],
                        close_time=time_now
                    )

            if b_signal > k1:
                long_order = self.order_manager.open_order(
                    code = code,
                    position = 1,
                    price = data.loc[time_now]['contract_close'],
                    open_time = time_now,
                    lot = lot,
                    slip = slip
                )
            if b_signal < -k1:
                short_order = self.order_manager.open_order(
                    code = code,
                    position = -1,
                    price = data.loc[time_now]['contract_close'],
                    open_time = time_now,
                    lot = lot,
                    slip = slip
                )

            if time_now.time() == time(15, 0):
                basis_org = data.loc[time_now]['basis']

        return data
