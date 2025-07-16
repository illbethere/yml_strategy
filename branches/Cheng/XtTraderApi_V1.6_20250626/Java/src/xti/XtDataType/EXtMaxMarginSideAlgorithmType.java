/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EXtMaxMarginSideAlgorithmType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 是否使用大额单边保证金算法
 *
 */
public enum EXtMaxMarginSideAlgorithmType {
    /**不使用大额单边保证金算法*/
    XT_FTDC_MMSA_NO(48),            
    /**使用大额单边保证金算法*/
    XT_FTDC_MMSA_YES(49);    

    public final int value;
    
    EXtMaxMarginSideAlgorithmType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
