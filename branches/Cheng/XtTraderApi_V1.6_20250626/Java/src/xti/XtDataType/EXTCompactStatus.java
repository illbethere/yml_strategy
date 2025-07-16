/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EXTCompactStatus.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 两融负债状态
 *
 */
public enum EXTCompactStatus {
	/**不限制*/
    COMPACT_STATUS_ALL(32),                 
    /**未归还*/
    COMPACT_STATUS_UNDONE(48),              
    /**部分归还*/
    COMPACT_STATUS_PART_DONE(49),           
    /**已归还*/
    COMPACT_STATUS_DONE(50),                
    /**自行了结*/
    COMPACT_STATUS_DONE_BY_SELF(51),        
    /**手工了结*/
    COMPACT_STATUS_DONE_BY_HAND(52),        
    /**未形成负债*/
    COMPACT_STATUS_NOT_DEBT(53),            
    /**到期未平仓*/
    COMPACT_STATUS_EXPIRY_NOT_CLOSE(54);    

    public final int value;
    
    EXTCompactStatus(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
