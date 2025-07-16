/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EMoneyType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/***
 * 
 * 币种
 *
 */
public enum EMoneyType {
	/**人民币*/
    MONEY_TYPE_RMB(48),      
    /**美元*/
    MONEY_TYPE_USD(49),      
    /**港币*/
    MONEY_TYPE_HK(50);       

    EMoneyType(int value) {
        this.value = value;
    }
    public final int value;
    public int value() {
        return this.value;
    }
}
