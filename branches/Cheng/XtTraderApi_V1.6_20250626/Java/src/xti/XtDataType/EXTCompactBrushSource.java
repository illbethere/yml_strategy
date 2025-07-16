/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EXTCompactBrushSource.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/***
 * 
 * 两融负债头寸来源
 *
 */
public enum EXTCompactBrushSource {
	/**不限制*/
    COMPACT_BRUSH_SOURCE_ALL(32),  
	/**普通头寸*/
    COMPACT_BRUSH_SOURCE_NORMAL(48),     
    /**专项头寸*/
    COMPACT_BRUSH_SOURCE_SPECIAL(49);      

    EXTCompactBrushSource(int value) {
        this.value = value;
    }
    public final int value;
    public int value() {
        return this.value;
    }
}
