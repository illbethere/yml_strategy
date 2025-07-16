import datetime

class OrderManager:
    def __init__(self, initial_capital, contract_size, margin_rate, max_position_ratio, 
                 fee_per_lot, slip_rate):
        self.open_orders = {}
        self.closed_orders = []
        self.order_id = 1
        self.money = initial_capital
        self.contract_size = contract_size
        self.margin_rate = margin_rate
        self.max_position_ratio = max_position_ratio
        self.fee_per_lot = fee_per_lot
        self.slip_rate = slip_rate
        self.equity = self.money

    def get_position_sum(self):
        long_orders = [order for order in self.open_orders.values() if order['position'] == 1]
        short_orders = [order for order in self.open_orders.values() if order['position'] == -1]

        long_margin = sum(order['value'] * self.margin_rate for order in long_orders)
        short_margin = sum(order['value'] * self.margin_rate for order in short_orders)

        return {
            'long_count': len(long_orders),
            'short_count': len(short_orders),
            'long_margin': long_margin,
            'short_margin': short_margin,
            'total_margin': long_margin + short_margin,
            'long_margin_ratio': long_margin / self.money,
            'short_margin_ratio': short_margin / self.money,
            'available_margin': self.money - (long_margin + short_margin)
        }
    
    def can_open_position(self, position: int, price: float, lot: int) -> dict:
        pos_summary = self.get_position_sum()

        new_value = price * self.contract_size * lot
        new_margin = new_value * self.margin_rate

        result = {
            'can_open': False,
            'tip': '',
            'new_margin': new_margin,
            'current_margin': pos_summary,
        }

        if new_margin > pos_summary['available_margin']:
            # result['tip'] = f"资金不足 --- 需要保证金->{new_margin:.2f}，可用保证金->{pos_summary['available_margin']:.2f}"
            return result

        if position == 1:  # 多头
            new_long_margin = pos_summary['long_margin'] + new_margin   
            new_long_ratio = new_long_margin / self.money

            if new_long_ratio > self.max_position_ratio:
                # result['tip'] = f"多头仓位过大 --- 新多头保证金->{new_long_margin:.2f}，占用资金比例->{new_long_ratio:.2%}，最大允许比例->{self.max_position_ratio:.2%}"
                # print(f"此时多头仓位：{pos_summary['long_count']}")
                return result
            
        elif position == -1:
            new_short_margin = pos_summary['short_margin'] + new_margin
            new_short_ratio = new_short_margin / self.money

            if new_short_ratio > self.max_position_ratio:
                # result['tip'] = f"空头仓位过大 --- 新空头保证金->{new_short_margin:.2f}，占用资金比例->{new_short_ratio:.2%}，最大允许比例->{self.max_position_ratio:.2%}"
                # print(f"此时空头仓位：{pos_summary['short_count']}")
                return result


        result['can_open'] = True
        result['tip'] = "可以开仓"
        return result
    

    def open_order(self, code: str, position: int, price: float, open_future_price:float, open_time: datetime, lot: int, slip: float) -> str: 

        #check_result = self.can_open_position(position, price, lot)

        #if not check_result['can_open']:
            # print(f"开仓失败 - {check_result['tip']}")
            #return None

        # 订单唯一ID
        order_id = f"{self.order_id:06d}"
        self.order_id += 1
        
        # 检查开仓方向
        if position == 1:
            price = price + price * slip
        elif position == -1:
            price = price - price * slip
        
        value = price*self.contract_size*lot
        open_fee = lot*self.fee_per_lot
        
        order_info = {
            'order_id':order_id,
            'code':code,
            'open_price':price,
            'open_future_price': open_future_price,
            'open_time':open_time,
            'position':position,
            'lot':lot, 
            'value':value, 
            'open_fee':open_fee,
            #'balance':balance,
            #'equity':equity
        } 

        self.open_orders[order_id] = order_info
        #print(f"开仓成功 - ID: {order_id} | 方向: {position} | 品种: {code} | 价格: {price} | 手数: {lot}")
        return order_id
    
    def close_order(self, order_id: str, price: float, close_time: datetime, slip: float = 0.0001) -> dict:
        
        if order_id not in self.open_orders:
            print(f"平仓失败 - 未找到订单ID: {order_id}")
            return None
    
        order = self.open_orders.pop(order_id) #取出并删除指定键对应的值！

        #平仓滑点计算
        if order['position'] == 1: #平多仓
            price = price - price * slip
            profit = (price - order['open_price'])*order['lot']*self.contract_size
        elif order['position'] == -1: #平空仓
            price = price + price * slip
            profit = (order['open_price'] - price)*order['lot']*self.contract_size
        
        #手续费计算
        close_fee = self.fee_per_lot * order['lot']
        
        net_profit = profit  - order['open_fee'] - close_fee
        self.equity = self.equity + net_profit
        
        closed_order = {
            **order,
            'close_price': price,
            'close_time': close_time,
            'profit': profit,
            'fee': order['open_fee'] + close_fee,
            'net_profit': net_profit,
            'equity' : self.equity,
            'position' : order['position'],
            'holding_period': (close_time - order['open_time']).total_seconds() / 3600
        }
        
        self.closed_orders.append(closed_order)
        
        #print(f"平仓成功 - ID: {order_id} | 方向: {order['position']} | "
             # f":手数: {order['lot']} | 开仓价: {order['open_price']} | "
              #f"平仓价: {price} | 净利润: {net_profit:.2f}")
        
        return closed_order