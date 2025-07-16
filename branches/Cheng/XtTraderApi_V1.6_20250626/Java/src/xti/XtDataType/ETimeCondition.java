/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   ETimeCondition.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtDataType;

/**
 * 
 * 期货时间条件单类型
 *
 */
public enum ETimeCondition {
	/**立即完成，否则撤销*/
    TIME_CONDITION_IOC(1),      
    /**本节有效*/
    TIME_CONDITION_GFS(2),      
    /**当日有效*/
    TIME_CONDITION_GFD(3),      
    /**指定日期前有效*/
    TIME_CONDITION_GTD(4),      
    /**撤销前有效*/
    TIME_CONDITION_GTC(5),      
    /**集合竞价有效*/
    TIME_CONDITION_GFA(6);      

    public final int value;
    
    ETimeCondition(int value) {
        this.value = value;
    }
    
    public int value() {
        return this.value;
    }
}
