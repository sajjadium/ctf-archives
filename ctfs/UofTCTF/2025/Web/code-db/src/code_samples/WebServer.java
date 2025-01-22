import java.io.*;
import java.net.*;
import java.util.concurrent.*;

public class AdvancedWebServer {
    private static final int PORT = 8080;
    private static ExecutorService threadPool = Executors.newFixedThreadPool(10);

    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(PORT);
        System.out.println("Advanced Web Server started on port " + PORT);

        while (true) {
            Socket client = serverSocket.accept();
            threadPool.execute(new ClientHandler(client));
        }
    }
}

class ClientHandler implements Runnable {
    private Socket client;

    ClientHandler(Socket socket) {
        this.client = socket;
    }

    public void run() {
        try (
            BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
            BufferedWriter out = new BufferedWriter(new OutputStreamWriter(client.getOutputStream()));
        ) {
            String line = in.readLine();
            if (line != null && line.startsWith("GET")) {
                String response = "HTTP/1.1 200 OK
" +
                                  "Content-Type: text/html

" +
                                  "<html><body><h1>Advanced Web Server</h1></body></html>";
                out.write(response);
                out.flush();
            }
            client.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
