/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EDualStatus.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 市场状态
 *
 */
public enum EDualStatus {
    /**无双中心*/
    E_DUAL_STATUS_NONE(-1),
    /**仅有上海*/
    E_DUAL_STATUS_SH(0),
    /**仅有深圳*/
    E_DUAL_STATUS_SZ(1),
    /**上海深圳双中心均有*/
    E_DUAL_STATUS_ALL(2);

    public final int value;
    
    EDualStatus(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
