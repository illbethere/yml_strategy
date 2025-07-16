/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EStopTradeForOwnHiLow.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/***
 * 
 * 涨跌停控制
 *
 */
public enum EStopTradeForOwnHiLow {
	/**主动算法是无，智能算法是最优价尽快执行*/
    STOPTRADE_NONE(0),      
    /**涨停不卖跌停不买*/
    STOPTRADE_NO_BUY_SELL(1),      
    /**原定时长执行*/
    STOPTRADE_SCHEDULED(2),      
    /**涨停不买跌停不卖*/
    STOPTRADE_NOT_CHASE(3);      

    EStopTradeForOwnHiLow(int value) {
        this.value = value;
    }
    public final int value;
    public int value() {
        return this.value;
    }
}
