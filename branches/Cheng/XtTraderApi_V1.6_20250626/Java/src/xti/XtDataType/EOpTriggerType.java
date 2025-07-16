/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EOpTriggerType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 下单价格类型
 *
 */
public enum EOpTriggerType {
    /**不使用触价*/
    OTT_NONE(0),                              
    /**向上触价*/
    OTT_UP(1),                              
    /**向下触价*/
    OTT_DOWN(2);

    public final int value;
    
    EOpTriggerType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
