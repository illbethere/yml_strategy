package test;

public class testJava 
{    
    public static void main(String[] args)
    {
    	String serverIpPort;
    	String username;
    	String password;
    	
    	if (args.length >= 3)
    	{
    		serverIpPort = args[0];
    		username = args[1];
    		password = args[2];
    	}
    	else
    	{
    		serverIpPort = "175.25.41.247:65300";
    		username = "api3";
    		password = "@a1234567";
    	}
    	
        Callback callback = new Callback(serverIpPort, username, password);
		System.out.println(System.getProperty("user.dir"));
		callback.init();
		callback.join();
		try {

			System.out.println("start sleep");
			Thread.sleep(100000);   // 休眠
			System.out.println("start end ");
		} catch (Exception e) {
			System.out.println("Got an exception!");
		}
    }
}
