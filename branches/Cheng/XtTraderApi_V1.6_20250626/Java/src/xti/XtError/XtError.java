/********************************************************************
      company:    北京睿智融科控股有限公司
      fileName:   XtError.java
      WARNING:    the code is machine generated, do not modify
*********************************************************************/

package xti.XtError;

/**
 * 
 * 错误信息，错误ID取值XT_ERROR_SUCCESS表示无错误
 *
 */
public class XtError {

    public XtError()
    {
    }
    public XtError(int errorID)
    {
        m_nErrorID = errorID;
    }
    public XtError(int errorID, String msg)
    {
        m_strErrorMsg = msg;
        m_nErrorID = errorID;
    }
	
	private long apiId;
    
    public long getApiId() {
        return this.apiId;
    }
    public void setApiId(long Id) {
        this.apiId = Id;
    }

    public void setErrorId(int id)
    {
        m_nErrorID = id;
    }
    public void setErrorMsg(String msg)
    {
        m_strErrorMsg = msg;
    }

    public boolean isSuccess()
    {
        return m_nErrorID == 0;
    }

    public int errorID()
    {
        return m_nErrorID;
    }
    public String errorMsg()
    {
        return m_strErrorMsg;
    }

    private int m_nErrorID;
    private String  m_strErrorMsg ;
}
