package org.d3ctf.demo;

import java.io.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;


@WebServlet(name = "systeminfo", value = "/systeminfo")
public class SystemInfo extends HttpServlet {
	public void init() {
    }

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("text/html");

        Runtime r = Runtime.getRuntime();
		Properties props = System.getProperties();
        String ip="", hostName = "";
        InetAddress addr = null;

        try {
			addr = InetAddress.getLocalHost();
		} catch (UnknownHostException e) {
			ip = "无法获取主机IP";
			hostName = "无法获取主机名";
		}
		if (null != addr) {
			try {
				ip = addr.getHostAddress();
			} catch (Exception e) {
				ip = "无法获取主机IP";
			}
			try {
				hostName = addr.getHostName();
			} catch (Exception e) {
				hostName = "无法获取主机名";
			}
		}
		
        // Hello
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<h1>System info</h1>");
        out.printf("Host ip: %s<br>", ip);
		out.printf("Host name: %s<br>", hostName);
		out.printf("Os name: %s<br>", props.getProperty("os.name"));
		out.printf("Arch: %s<br>", props.getProperty("os.arch"));
		out.printf("Os version: %s<br>", props.getProperty("os.version"));
		out.printf("Processors: %s<br>", r.availableProcessors());
		out.printf("Java version: %s<br>", props.getProperty("java.version"));
		out.printf("Vendor: %s<br>", props.getProperty("java.vendor"));
		out.printf("Java URL: %s<br>", props.getProperty("java.vendor.url"));
		out.printf("Java home: %s<br>", props.getProperty("java.home"));
		out.printf("Tmp dir: %s<br>", props.getProperty("java.io.tmpdir"));
		out.printf("Listen port: %d<br>", request.getLocalPort());
        out.println("</body></html>");

    }

    public void destroy() {
    }
	
	

}