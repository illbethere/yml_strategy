/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EXTCompactType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 两融负债类型
 *
 */
public enum EXTCompactType {
	/**不限制*/
    COMPACT_TYPE_ALL(32),  
    /**融资*/
    COMPACT_TYPE_FIN(48),  
    /**融券*/
    COMPACT_TYPE_SLO(49);  

    public final int value;
    
    EXTCompactType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
