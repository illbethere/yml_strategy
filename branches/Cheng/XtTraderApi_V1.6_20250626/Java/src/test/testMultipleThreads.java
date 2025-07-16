package test;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class testMultipleThreads {

    private static final int CORE_POOL_SIZE = 10; //线程池的核心线程数量
    private static final int MAX_POOL_SIZE = 20;  //线程池的最大线程数
    private static final int QUEUE_CAPACITY = 100;
    private static final long KEEP_ALIVE_TIME = 1L; //当线程数大于核心线程数时，多余的空闲线程存活的最长时间

    public static void main(String[] args) {
        String serverIpPort;
        String username;
        String password;

        if (args.length >= 3) {
            serverIpPort = args[0];
            username = args[1];
            password = args[2];
        } else {
            serverIpPort = "175.25.41.247:65300";
            username = "api";
            password = "@a123456";
        }

        ThreadPoolExecutor pool = new ThreadPoolExecutor(
                CORE_POOL_SIZE,
                MAX_POOL_SIZE,
                KEEP_ALIVE_TIME,
                TimeUnit.SECONDS,
                new ArrayBlockingQueue<>(QUEUE_CAPACITY),
                new ThreadPoolExecutor.CallerRunsPolicy());

        //多线程多实例
        for (int callbackNums = 0; callbackNums < 30; callbackNums++) {
            pool.execute(() -> {
                System.out.println("Enter run() ");
                Callback callback = new Callback(serverIpPort, username, password);
                System.out.println(System.getProperty("user.dir"));
                if (callback.init()) {
                    callback.join();
                } else {
                    System.out.println("Init TraderApi failure, exit");
                }
            });
        }


        pool.shutdown();

        System.out.println("main over");
    }
}


