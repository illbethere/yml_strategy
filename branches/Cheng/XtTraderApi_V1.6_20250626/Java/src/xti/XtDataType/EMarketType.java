/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EErrorType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 市场定义
 */
public enum EMarketType {
	/** 上交所 */
    MARKET_SHANGHAI("SH"),                  
    /** 深交所*/
    MARKET_SHENZHEN("SZ"),                  
    /** 股指期货*/
    MARKET_INDEX_FUTURE("CFFEX"),           
    /** 上海商品期货*/
    MARKET_SHANGHAI_FUTURE("SHFE"),         
    /** 大连商品期货*/
    MARKET_DALIAN_FUTURE("DCE"),            
    /** 郑州商品期货*/
    MARKET_ZHENGZHOU_FUTURE("CZCE"),        
    /** 上海期权*/
    MARKET_SHANGHAI_STOCK_OPTION("SHO"),    
    /** 深圳期权*/
    MARKET_SHENZHEN_STOCK_OPTION("SZO"),    
    /** 沪港通*/
    MARKET_SHANGHAI_HONGKONG_STOCK("HGT"),    
    /** 深港通*/
    MARKET_SHENZHEN_HONGKONG_STOCK("SGT"),
    /** 国际能源中心期货*/
    MARKET_INTL_ENERGY_FUTURE("INE"),

    /** 北京证券交易所*/
    MARKET_BEIJING("BJ"),

    /** 新三板*/
    MARKET_NEEQ("NEEQ");

    public final String value;
    
    EMarketType(String value) {
        this.value = value;
    }
    
    public String value() {
        return this.value;
    }
}
