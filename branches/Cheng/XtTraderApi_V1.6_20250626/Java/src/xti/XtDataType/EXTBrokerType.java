/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EXTBrokerType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 账号类型
 *
 */
public enum EXTBrokerType {
	/**期货账号*/
    AT_FUTURE(1),          
    /**股票账号*/
    AT_STOCK(2),           
    /**信用账号*/
    AT_CREDIT(3),          
    /**贵金属账号*/
    AT_GOLD(4),            
    /**期货期权账号*/
    AT_FUTURE_OPTION(5),   
    /**股票期权账号*/
    AT_STOCK_OPTION(6),    
    /**沪港通账号*/
    AT_HUGANGTONG(7),      
    /**美股收益互换账号*/
    AT_INCOME_SWAP(8),      
    /**全国股转账号*/
    AT_NEW3BOARD(10),     
    /**深港通账号*/
    AT_SHENGANGTONG(11),
    /**深港通账号*/
    AT_FICC_COMMODITY(14),
    /**深港通账号*/
    AT_FICC_INTEREST(15); 

    public final int value;
    
    EXTBrokerType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
