#include <stdlib.h>
#include <demo1/CallBackDemo1.h>
#include <demo2/CallBackDemo2.h>
#include <demo3/CallBackDemo3.h>
#include <demo4/CallBackDemo4.h>
#include <demo5/CallBackDemo5.h>
#include <demo6/CallBackDemo6.h>
#include <demo7/CallBackDemo7.h>
#include <demo8/CallBackDemo8.h>

using namespace std;

// 初始化、登录、获取资金账号
void run_demo1(const std::string& address, const std::string& username, const std::string& password)
{
    demo1::Callback* pCallback = new demo1::Callback(address, username, password);
    pCallback->init();
    pCallback->join();
    delete pCallback;
}

// 查询资金账号信息、查询产品信息
void run_demo2(const std::string& address, const std::string& username, const std::string& password)
{
    demo2::Callback* pCallback = new demo2::Callback(address, username, password);
    pCallback->init();
    pCallback->join();
    delete pCallback;
}

// 订阅行情，股票普通下单，期货普通下单
void run_demo3(const std::string& address, const std::string& username, const std::string& password)
{
    demo3::Callback* pCallback = new demo3::Callback(address, username, password);
    pCallback->init();
    pCallback->join();
    delete pCallback;
}

// 撤单
void run_demo4(const std::string& address, const std::string& username, const std::string& password)
{
    demo4::Callback* pCallback = new demo4::Callback(address, username, password);
    pCallback->init();
    pCallback->join();
    delete pCallback;
}

// 算法下单
void run_demo5(const std::string& address, const std::string& username, const std::string& password)
{
    demo5::Callback* pCallback = new demo5::Callback(address, username, password);
    pCallback->init();
    pCallback->join();
    delete pCallback;
}

// 定时器下单
void run_demo6(const std::string& address, const std::string& username, const std::string& password)
{
    demo6::Callback* pCallback = new demo6::Callback(address, username, password);
    pCallback->init();
    pCallback->join();
    delete pCallback;
}

// 实现全部接口
void run_demo7(const std::string& address, const std::string& username, const std::string& password)
{
    demo7::Callback* pCallback = new demo7::Callback(address, username, password);
    pCallback->init();
    pCallback->join();
    delete pCallback;
}

// 实现全部接口
void run_demo7(const std::string& address, const std::string& username, const std::string& password, const std::string& username1, const std::string& password1, const std::string& username2, const std::string& password2, const std::string& username3, const std::string& password3, const std::string& username4, const std::string& password4)
{
    demo7::Callback* pCallback = new demo7::Callback(address, username, password);
    pCallback->init();
    demo7::Callback* pCallback1 = new demo7::Callback(address, username1, password1);
    pCallback1->init();
    demo7::Callback* pCallback2 = new demo7::Callback(address, username2, password2);
    pCallback2->init();
    demo7::Callback* pCallback3 = new demo7::Callback(address, username3, password3);
    pCallback3->init();
    demo7::Callback* pCallback4 = new demo7::Callback(address, username4, password4);
    pCallback4->init();
    pCallback->joinAll();
    delete pCallback;
    delete pCallback2;

}

// 创建多实例，主线程创建
void run_demo8(const std::string& address, const std::string& username, const std::string& password)
{
    // 测试代码，创建两个相同用户的实例，多实例时填具体的用户名和密码
    demo8::Callback* pCallback = new demo8::Callback(address, username, password);
    pCallback->init();
    demo8::Callback* pCallback1 = new demo8::Callback(address, username, password);
    pCallback1->init();

    // 启动多实例线程
    XtTraderApi::joinAll();
    delete pCallback;
}

int main(int argc, char* argv[])
{
    string serverIpPort;
    string username;
    string password;
    string username1;
    string password1;
    string username2;
    string password2;
    string username3;
    string password3;
    string username4;
    string password4;
    int demoNum = 7;
    if (argc < 5)
    {
        serverIpPort = "175.25.41.247:65300";
        username = "api4";
        password = "@a1234567";
    }
    else
    {
        serverIpPort = argv[1];
        username = argv[2];
        password = argv[3];
        demoNum = atoi(argv[4]);
    }

    switch (demoNum)
    {
    case 1:
        // 初始化、登录、获取资金账号
        run_demo1(serverIpPort, username, password);
        break;
    case 2:
        // 查询资金账号信息、查询产品信息
        run_demo2(serverIpPort, username, password);
        break;
    case 3:
        // 订阅行情，股票普通下单，期货普通下单
        run_demo3(serverIpPort, username, password);
        break;
    case 4:
        // 撤单
        run_demo4(serverIpPort, username, password);
        break;
    case 5:
        // 算法下单
        run_demo5(serverIpPort, username, password);
        break;
    case 6:
        // 定时器下单
        run_demo6(serverIpPort, username, password);
        break;
    case 7:
        // 实现全部接口
        if (username2.empty())
        {
            run_demo7(serverIpPort, username, password);
        }
        else
        { 
            run_demo7(serverIpPort, username, password, username1, password1, username2, password2, username3, password3, username4, password4);
        }
    case 8:
        // 多实例
        run_demo8(serverIpPort, username, password);
        break;
    default:
        break;
    }

    return 0;
}
