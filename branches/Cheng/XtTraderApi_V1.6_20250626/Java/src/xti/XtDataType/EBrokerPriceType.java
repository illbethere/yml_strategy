/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EBrokerPriceType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 委托明细价格类型
 *
 */
public enum EBrokerPriceType {
	/**市价*/
    BROKER_PRICE_ANY(49),                       
    /**限价*/
    BROKER_PRICE_LIMIT(50),                     
    /**最优价*/
    BROKER_PRICE_BEST(51),                      
    /**配股*/
    BROKER_PRICE_PROP_ALLOTMENT(52),            
    /**转托*/
    BROKER_PRICE_PROP_REFER(53),                
    /**申购*/
    BROKER_PRICE_PROP_SUBSCRIBE(54),            
    /**回购*/
    BROKER_PRICE_PROP_BUYBACK(55),              
    /**配售*/
    BROKER_PRICE_PROP_PLACING(56),              
    /**指定*/
    BROKER_PRICE_PROP_DECIDE(57),               
    /**转股*/
    BROKER_PRICE_PROP_EQUITY(58),               
    /**回售*/
    BROKER_PRICE_PROP_SELLBACK(59),             
    /**股息*/
    BROKER_PRICE_PROP_DIVIDEND(60),             
    /**深圳配售确认*/
    BROKER_PRICE_PROP_SHENZHEN_PLACING(68),     
    /**配售放弃*/
    BROKER_PRICE_PROP_CANCEL_PLACING(69),       
    /**无冻质押*/
    BROKER_PRICE_PROP_WDZY(70),                 
    /**冻结质押*/
    BROKER_PRICE_PROP_DJZY(71),                 
    /**无冻解押*/
    BROKER_PRICE_PROP_WDJY(72),                 
    /**解冻解押*/
    BROKER_PRICE_PROP_JDJY(73),                 
    /**投票*/
    BROKER_PRICE_PROP_VOTE(75),                 
    /**要约收购预售*/
    BROKER_PRICE_PROP_YYSGYS(76),               
    /**预售要约解除*/
    BROKER_PRICE_PROP_YSYYJC(77),               
    /**基金设红*/
    BROKER_PRICE_PROP_FUND_DEVIDEND(78),        
    /**基金申赎*/
    BROKER_PRICE_PROP_FUND_ENTRUST(79),         
    /**跨市转托*/
    BROKER_PRICE_PROP_CROSS_MARKET(80),         
    /**ETF申购*/
    BROKER_PRICE_PROP_ETF(81),                  
    /**权证行权*/
    BROKER_PRICE_PROP_EXERCIS(83),              
    /**对手方最优价格*/
    BROKER_PRICE_PROP_PEER_PRICE_FIRST(84),     
    /**最优五档即时成交剩余转限价*/
    BROKER_PRICE_PROP_L5_FIRST_LIMITPX(85),     
    /**本方最优价格*/
    BROKER_PRICE_PROP_MIME_PRICE_FIRST(86),     
    /**即时成交剩余撤销*/
    BROKER_PRICE_PROP_INSTBUSI_RESTCANCEL(87),  
    /**最优五档即时成交剩余撤销*/
    BROKER_PRICE_PROP_L5_FIRST_CANCEL(88),      
    /**全额成交并撤单*/
    BROKER_PRICE_PROP_FULL_REAL_CANCEL(89),     
    /**基金拆合*/
    BROKER_PRICE_PROP_FUND_CHAIHE(90),
    /**涨跌停价*/
    BROKER_PRICE_PROP_MARKET(130),
    /**最优价*/
    BROKER_PRICE_PROP_MARKET_BEST(131),
    /**市价_即成剩撤*/
    BROKER_PRICE_PROP_MARKET_CANCEL(132),
    /**市价_全额成交或撤*/
    BROKER_PRICE_PROP_MARKET_CANCEL_ALL(133),
    /**市价_最优1档即成剩撤*/
    BROKER_PRICE_PROP_MARKET_CANCEL_1(134),
    /**市价_最优5档即成剩撤*/
    BROKER_PRICE_PROP_MARKET_CANCEL_5(135),
    /**市价_最优1档即成剩转*/
    BROKER_PRICE_PROP_MARKET_CONVERT_1(136),
    /**市价_最优5档即成剩转*/
    BROKER_PRICE_PROP_MARKET_CONVERT_5(137),
    /**股票期权-询价*/
    BROKER_PRICE_PROP_STK_OPTION_ASK(138),
    /**股票期权-限价即时全部成交否则撤单*/
    BROKER_PRICE_PROP_STK_OPTION_FIX_CANCEL_ALL(139),
    /**票期权-市价即时成交剩余撤单*/
    BROKER_PRICE_PROP_STK_OPTION_MARKET_CACEL_LEFT(140),
    /**股票期权-市价即时全部成交否则撤单*/
    BROKER_PRICE_PROP_STK_OPTION_MARKET_CANCEL_ALL(141),
    /**股票期权-市价剩余转限价*/
    BROKER_PRICE_PROP_STK_OPTION_MARKET_CONVERT_FIX(142),
    /**股票期权-组合行权*/
    BROKER_PRICE_PROP_OPTION_COMB_EXERCISE(164),
    /**股票期权-构建认购牛市价差策略*/
    BROKER_PRICE_PROP_OPTION_BUILD_COMB_STRATEGY_CNSJC(165),
    /**股票期权-构建认沽熊市价差策略*/
    BROKER_PRICE_PROP_OPTION_BUILD_COMB_STRATEGY_PXSJC(166),
    /**股票期权-构建认沽牛市价差策略*/
    BROKER_PRICE_PROP_OPTION_BUILD_COMB_STRATEGY_PNSJC(167),
    /**股票期权-构建认购熊市价差策略*/
    BROKER_PRICE_PROP_OPTION_BUILD_COMB_STRATEGY_CXSJC(168),
    /**股票期权-构建跨式空头策略*/
    BROKER_PRICE_PROP_OPTION_BUILD_COMB_STRATEGY_KS(169),
    /**股票期权-构建宽跨式空头策略*/
    BROKER_PRICE_PROP_OPTION_BUILD_COMB_STRATEGY_KKS(170),
    /**股票期权-普通转备兑*/
    BROKER_PRICE_PROP_OPTION_BUILD_COMB_STRATEGY_ZBD(171),
    /**股票期权-备兑转普通*/
    BROKER_PRICE_PROP_OPTION_BUILD_COMB_STRATEGY_ZXJ(172),
    /**股票期权-解除认购牛市价差策略*/
    BROKER_PRICE_PROP_OPTION_RELEASE_COMB_STRATEGY_CNSJC(173),
    /**股票期权-解除认沽熊市价差策略*/
    BROKER_PRICE_PROP_OPTION_RELEASE_COMB_STRATEGY_PXSJC(174),
    /**股票期权-解除认沽牛市价差策略*/
    BROKER_PRICE_PROP_OPTION_RELEASE_COMB_STRATEGY_PNSJC(175),
    /**股票期权-解除认购熊市价差策略*/
    BROKER_PRICE_PROP_OPTION_RELEASE_COMB_STRATEGY_CXSJC(176),
    /**股票期权-解除跨式空头策略*/
    BROKER_PRICE_PROP_OPTION_RELEASE_COMB_STRATEGY_KS(177),
    /**股票期权-解除宽跨式空头策略*/
    BROKER_PRICE_PROP_OPTION_RELEASE_COMB_STRATEGY_KKS(178),
    _C_BRPT_COUNT(179);

    public final int value;
    
    EBrokerPriceType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
