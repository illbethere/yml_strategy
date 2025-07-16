/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EXtOverFreqOrderMode.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 下单超过流控时处理方式
 *
 */
public enum EXtOverFreqOrderMode {
	/**禁止*/
    OFQ_FORBID(0),  
    /**队列*/
    OFQ_QUEUE(1);   

    public final int value;
    
    EXtOverFreqOrderMode(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
