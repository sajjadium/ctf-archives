using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

class ChatServer
{
    static void Main()
    {
        TcpListener server = new TcpListener(IPAddress.Any, 5000);
        server.Start();
        Console.WriteLine("Chat server started on port 5000.");

        while (true)
        {
            TcpClient client = server.AcceptTcpClient();
            Console.WriteLine("Client connected.");
            Thread thread = new Thread(HandleClient);
            thread.Start(client);
        }
    }

    static void HandleClient(object obj)
    {
        TcpClient client = (TcpClient)obj;
        NetworkStream stream = client.GetStream();
        byte[] buffer = new byte[1024];
        int byteCount;

        while((byteCount = stream.Read(buffer, 0, buffer.Length)) > 0){
            string data = Encoding.UTF8.GetString(buffer, 0, byteCount);
            Console.WriteLine("Received: " + data);
            byte[] response = Encoding.UTF8.GetBytes("Echo: " + data);
            stream.Write(response, 0, response.Length);
        }

        client.Close();
        Console.WriteLine("Client disconnected.");
    }
}
