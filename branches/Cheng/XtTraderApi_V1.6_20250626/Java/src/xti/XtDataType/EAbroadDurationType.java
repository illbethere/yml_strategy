/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EAbroadDurationType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 外盘期货报价类型
 *
 */
public enum EAbroadDurationType {
	/**市价单*/
    TYPE_DURATION_MKT(48),
    /**限价单*/
    TYPE_DURATION_LMT(49),
    /**竞价单*/
    TYPE_DURATION_AO(50),
	/**竞价限价单*/
    TYPE_DURATION_ALO(51),
    /**增强限价单*/
    TYPE_DURATION_ELO(52),
    /**特别限价盘单*/
    TYPE_DURATION_SLO(53),
    /**碎股限价单*/
    TYPE_DURATION_OLI(54);

    public final int value;
    
    EAbroadDurationType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
