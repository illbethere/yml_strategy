/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EAlgoPriceType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 普通算法订单类型
 *
 */
public enum EAlgoPriceType {
    /**市价*/
    EALGO_PRT_MARKET(0),
    /**限价*/
    EALGO_PRT_FIX(2);

    public final int value;
    
    EAlgoPriceType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
