/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EOrderStrategyType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/***
 * 
 * 算法下单方式
 *
 */
public enum EOrderStrategyType {
	/**普通*/
    E_ORDER_STRATEGY_TYPE_NORMAL(-1),      
    /**近场交易，需要服务支持*/
    E_ORDER_STRATEGY_TYPE_APPROACH(0);      

    EOrderStrategyType(int value) {
        this.value = value;
    }
    public final int value;
    public int value() {
        return this.value;
    }
}
