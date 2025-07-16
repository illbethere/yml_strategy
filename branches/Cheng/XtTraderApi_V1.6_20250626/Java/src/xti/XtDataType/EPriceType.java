/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EPriceType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 下单价格类型
 *
 */
public enum EPriceType {
	/**无效*/
    PRTP_INVALID(-1),
    /**卖5*/
    PRTP_SALE5(0),                              
    /**卖4*/
    PRTP_SALE4(1),                              
    /**卖3*/
    PRTP_SALE3(2),                              
    /**卖2*/
    PRTP_SALE2(3),                              
    /**卖1*/
    PRTP_SALE1(4),                              
    /**最新价*/
    PRTP_LATEST(5),                             
    /**买1*/
    PRTP_BUY1(6),                               
    /**买2*/
    PRTP_BUY2(7),                               
    /**买3*/
    PRTP_BUY3(8),                               
    /**买4*/
    PRTP_BUY4(9),                               
    /**买5*/
    PRTP_BUY5(10),                              
    /**指定价*/
    PRTP_FIX(11),                              
    /**市价*/
    PRTP_MARKET(12),                           
    /**挂单价 跟盘价*/
    PRTP_HANG(13),                              
    /**对手价*/
    PRTP_COMPETE(14),                           
    
    /**期货市价*/
    /**市价_最优价 郑商所*/
    PRTP_MARKET_BEST(18),                      
    /**市价_即成剩撤 大商所*/
    PRTP_MARKET_CANCEL(19),                    
    /**市价_全额成交或撤 大商所*/
    PRTP_MARKET_CANCEL_ALL(20),                 
    /**市价_最优1档即成剩撤 中金所*/
    PRTP_MARKET_CANCEL_1(21),                   
    /**市价_最优5档即成剩撤 中金所 上期所*/
    PRTP_MARKET_CANCEL_5(22),                   
    /**市价_最优1档即成剩转 中金所*/
    PRTP_MARKET_CONVERT_1(23),                  
    /**市价_最优5档即成剩转 中金所 上期所*/
    PRTP_MARKET_CONVERT_5(24),                  
    /**限价即时全部成交否则撤单*/
    PRTP_STK_OPTION_FIX_CANCEL_ALL(26),
    /**上海股票期权市价*/
    /**市价即时成交剩余撤单*/
    PRTP_STK_OPTION_MARKET_CACEL_LEFT(27),      
    /**市价即时全部成交否则撤单*/
    PRTP_STK_OPTION_MARKET_CANCEL_ALL(28),      
    /**市价剩余转限价*/
    PRTP_STK_OPTION_MARKET_CONVERT_FIX(29),     
    
    /**上海股票市价*/
    /**最优五档即时成交剩余撤销*/
    PRTP_MARKET_SH_CONVERT_5_CANCEL(42),        
    /**最优五档即时成交剩转限价*/
    PRTP_MARKET_SH_CONVERT_5_LIMIT(43),         
    
    /**深圳股票期权和深圳股票市价*/
    /**对手方最优价格委托，可用于上海科创板市价*/
    PRTP_MARKET_PEER_PRICE_FIRST(44),           
    /**本方最优价格委托，可用于上海科创板市价*/
    PRTP_MARKET_MINE_PRICE_FIRST(45),           
    /**即时成交剩余撤销委托*/
    PRTP_MARKET_SZ_INSTBUSI_RESTCANCEL(46),     
    /**最优五档即时成交剩余撤销委托*/
    PRTP_MARKET_SZ_CONVERT_5_CANCEL(47),        
    /**全额成交或撤销委托*/
    PRTP_MARKET_SZ_FULL_REAL_CANCEL(48),        
    /**盘后定价申报*/
    PRTP_AFTER_FIX_PRICE(49),                   
    
    /**股票期权组合保证金策略*/
    /**股票期权-认购牛市价差策略*/
    PRTP_OPTION_COMB_STRATEGY_CNSJC(50),        
    /**股票期权-认沽熊市价差策略*/
    PRTP_OPTION_COMB_STRATEGY_PXSJC(51),        
    /**股票期权-认沽牛市价差策略*/
    PRTP_OPTION_COMB_STRATEGY_PNSJC(52),        
    /**股票期权-认购熊市价差策略*/
    PRTP_OPTION_COMB_STRATEGY_CXSJC(53),        
    /**股票期权-跨式空头*/
    PRTP_OPTION_COMB_STRATEGY_KS(54),           
    /**股票期权-宽跨式空头*/
    PRTP_OPTION_COMB_STRATEGY_KKS(55),          
    /**股票期权-保证金开仓转备兑开仓*/
    PRTP_OPTION_COMB_STRATEGY_ZBD(56),          
    
    PRTP_OPTION_COMB_STRATEGY_ZXJ(57),          
    
    _C_PRTP_COUNT(58);

    public final int value;
    
    EPriceType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
