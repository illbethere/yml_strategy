/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   EPortfolioType.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 投组类型
 *
 */
public enum EPortfolioType {
	/**普通*/
	PF_TYPE_NORMAL(0),           
    /**用户默认*/
	PF_TYPE_USER(1),          
    /**账号默认*/
    PF_TYPE_ACCOUNT(2);    

    public final int value;
    
    EPortfolioType(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
