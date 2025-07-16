/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EOperationType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 下单类型
 *
 */
public enum EOperationType {
    OPT_INVALID(-1),
    
    /** 期货业务*/
    /**开多 0*/
    OPT_OPEN_LONG(0),                       
    /**平昨多 1*/
    OPT_CLOSE_LONG_HISTORY(1),              
    /**平今多 2*/
    OPT_CLOSE_LONG_TODAY(2),                
    /**开空 3*/
    OPT_OPEN_SHORT(3),                      
    /**平昨空 4*/
    OPT_CLOSE_SHORT_HISTORY(4),             
    /**平今空 5*/
    OPT_CLOSE_SHORT_TODAY(5),               
    /**平多，优先平今  6*/
    OPT_CLOSE_LONG_TODAY_FIRST(6),          
    /**平多，优先平昨 7*/
    OPT_CLOSE_LONG_HISTORY_FIRST(7),        
    /**平空，优先平今 8*/
    OPT_CLOSE_SHORT_TODAY_FIRST(8),         
    /**平空，优先平昨 9*/
    OPT_CLOSE_SHORT_HISTORY_FIRST(9),       
    /**开空，优先平今多*/
    OPT_CLOSE_LONG_TODAY_HISTORY_THEN_OPEN_SHORT(10),       
    /**开空，优先平昨多*/
    OPT_CLOSE_LONG_HISTORY_TODAY_THEN_OPEN_SHORT(11),       
    /**开多，优先平今空*/
    OPT_CLOSE_SHORT_TODAY_HISTORY_THEN_OPEN_LONG(12),       
    /**开多，优先平昨空*/
    OPT_CLOSE_SHORT_HISTORY_TODAY_THEN_OPEN_LONG(13),       
    /** 卖出，优先开仓*/
    OPT_SELL_PRIORITY_OPEN(14),       
    /**买入，优先开仓*/
    OPT_BUY_PRIORITY_OPEN(15),       
    /**卖出，最优手续费*/
    OPT_SELL_OPTIMAL_COMSSION(16),       
    /**买入，最优手续费*/
    OPT_BUY_OPTIMAL_COMSSION(17),       

    /**股票业务*/
    /**买入，针对股票 18*/
    OPT_BUY(18),                            
    /**卖出，针对股票 19*/
    OPT_SELL(19),                           
    
    /**信用交易*/
    /**融资买入*/
    OPT_FIN_BUY(20),                        
    /**融券卖出*/
    OPT_SLO_SELL(21),                       
    /**买券还券*/
    OPT_BUY_SECU_REPAY(22),                 
    /**直接还券*/
    OPT_DIRECT_SECU_REPAY(23),              
    /**卖券还款*/
    OPT_SELL_CASH_REPAY(24),                
    /**直接还款*/
    OPT_DIRECT_CASH_REPAY(25),              
    
    /**分级基金*/
    /**基金申购*/
    OPT_FUND_SUBSCRIBE(26),                 
    /**基金赎回*/
    OPT_FUND_REDEMPTION(27),                
    /**基金合并*/
    OPT_FUND_MERGE(28),                     
    /**基金分拆*/
    OPT_FUND_SPLIT(29),                     
    
    /**正回购*/
    /**质押入库*/
    OPT_PLEDGE_IN(30),                      
    /**质押出库*/
    OPT_PLEDGE_OUT(31),                     
    
    /**期权业务*/
    /**买入开仓*/
    OPT_OPTION_BUY_OPEN(32),                
    /**卖出平仓*/
    OPT_OPTION_SELL_CLOSE(33),              
    /**卖出开仓*/
    OPT_OPTION_SELL_OPEN(34),               
    /**买入平仓*/
    OPT_OPTION_BUY_CLOSE(35),               
    /**备兑开仓*/
    OPT_OPTION_COVERED_OPEN(36),            
    /**备兑平仓*/
    OPT_OPTION_COVERED_CLOSE(37),           
    /**认购行权*/
    OPT_OPTION_CALL_EXERCISE(38),           
    /**认沽行权*/
    OPT_OPTION_PUT_EXERCISE(39),            
    /**证券锁定*/
    OPT_OPTION_SECU_LOCK(40),               
    /**证券解锁*/
    OPT_OPTION_SECU_UNLOCK(41),             
    
    /**期货期权*/
    /**期货期权行权*/
    OPT_FUTURE_OPTION_EXERCISE(50),         

    /**可转债转股*/
    OPT_CONVERT_BONDS(51),
    /**可转债回售*/
    OPT_SELL_BACK_BONDS(51),
    
    /**担保品划转*/
    /**担保品划入*/
    OPT_COLLATERAL_TRANSFER_IN(55),         
    /**担保品划出*/
    OPT_COLLATERAL_TRANSFER_OUT(56),        
    
    /**ETF业务*/
    /**ETF申购*/
    OPT_ETF_PURCHASE(1004),                 
    /**ETF赎回*/
    OPT_ETF_REDEMPTION(1005),               
    
    /**科创板和创业板盘后定价业务*/
    /**盘后定价买入*/
    OPT_AFTER_FIX_BUY(1043),                
    /**盘后定价卖出*/
    OPT_AFTER_FIX_SELL(1044),               
    
    /**期权组合*/
    /**组合行权*/
    OPT_OPTION_COMB_EXERCISE(1089),         
    /**构建组合策略*/
    OPT_OPTION_BUILD_COMB_STRATEGY(1890),   
    /**解除组合策略*/
    OPT_OPTION_RELEASE_COMB_STRATEGY(1891), 
    
    /**信用专项交易*/
    /**专项融券卖出*/
    OPT_SLO_SELL_SPECIAL(1010),         
    /**专项买券还券*/
    OPT_BUY_SECU_REPAY_SPECIAL(1011),   
    /**专项直接还券*/
    OPT_DIRECT_SECU_REPAY_SPECIAL(1012), 
    /**专项融资买入*/
    OPT_FIN_BUY_SPECIAL(1022),         
    /**专项卖券还款*/
    OPT_SELL_CASH_REPAY_SPECIAL(1023),   
    /**专项直接还款*/
    OPT_DIRECT_CASH_REPAY_SPECIAL(1024),
    /**买入优先平仓*/
    OPT_OPTION_BUY_CLOSE_THEN_OPEN(1154),
    /**卖出优先平仓*/
    OPT_OPTION_SELL_CLOSE_THEN_OPEN(1155);

    public final int value;
    
    EOperationType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
