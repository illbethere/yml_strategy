/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   JTaskOpRecord.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtStructs;

import xti.XtDataType.ETaskFlowOperation;

/**
* JTaskOpRecord类
* 任务操作
*/
public class JTaskOpRecord{
    /**
    * 指令ID
    */
    public int m_nCmdId;
    /**
    * 任务操作
    */
    public ETaskFlowOperation m_eOperator;
    /**
    * 操作原因
    */
    public String m_strReason;

    /**
    * 设置任务操作
    * @param m_eOperator 任务操作
    */
    public void setM_eOperator(ETaskFlowOperation m_eOperator) {
        this.m_eOperator = m_eOperator;
    }
}
