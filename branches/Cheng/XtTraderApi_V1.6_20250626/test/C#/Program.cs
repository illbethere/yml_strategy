using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using NetApi;

namespace test4csharp
{
    class Program
    {
        static void Main(string[] args)
        {
            // String address, String username, String password, String accountid, int orderNum(每秒钟下单量), int timeSec(秒数)
            Callback pcallback = new Callback("175.25.41.247:65300", "api3", "@a1234567", "2000463", 1, 1);
            if (pcallback.init())
            {
                pcallback.join();
            }
        }
    }
}
