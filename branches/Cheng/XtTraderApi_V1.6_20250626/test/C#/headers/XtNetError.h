/********************************************************************
    company:        北京睿智融科控股有限公司
    fileName:       XtNetError.h
    author:         xujun
    created:        02:25:2015     9:51
    purpose:        错误
*********************************************************************/
#ifndef XTNETERROR_2015_02_25_H
#define XTNETERROR_2015_02_25_H

using namespace System;

namespace NetApi
{
    public ref class XtError
    {
    public:
        XtError(){}
        XtError(int errorID){m_nErrorID = errorID;}
        XtError(int errorID, String^ msg){m_nErrorID = errorID; m_strErrorMsg = msg;}

        void setErrorId(int id){m_nErrorID = id;}
        void setErrorMsg(String^ msg){m_strErrorMsg = msg;}

        bool isSuccess()
        {
            return 0 == m_nErrorID;
        }

        int errorID(){return m_nErrorID;};
        String^ errorMsg(){return m_strErrorMsg;}

        bool operator!(){return !isSuccess();}  // true if no error

    protected:
    private:
        int m_nErrorID;
        String^ m_strErrorMsg;
    };
}

#endif
