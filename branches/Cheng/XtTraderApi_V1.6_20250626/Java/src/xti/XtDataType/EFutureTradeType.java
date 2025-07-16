/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EFutureTradeType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 期货交易类型
 *
 */
public enum EFutureTradeType {
	/**普通成交*/
    FUTRUE_TRADE_TYPE_COMMON(48),               
    /**期权成交*/
    FUTURE_TRADE_TYPE_OPTIONSEXECUTION(49),     
    /**OTC成交*/
    FUTURE_TRADE_TYPE_OTC(50),                  
    /**期转现衍生成交*/
    FUTURE_TRADE_TYPE_EFPDIRVED(51),            
    /**组合衍生成交*/
    FUTURE_TRADE_TYPE_COMBINATION_DERIVED(52);  

    public final int value;
    
    EFutureTradeType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
