package cscg;

import java.io.File;
 
import javax.servlet.ServletException;
 
import org.apache.catalina.LifecycleException;
import org.apache.catalina.WebResourceRoot;
import org.apache.catalina.core.StandardContext;
import org.apache.catalina.startup.Tomcat;
import org.apache.catalina.webresources.DirResourceSet;
import org.apache.catalina.webresources.StandardRoot;

public class EmbeddedTomcat {
 
   
    public static void main(String[] args) throws LifecycleException, ServletException {
        String contextPath = "/";
        String webappDir = new File("WebContent").getAbsolutePath();

        Tomcat tomcat = new Tomcat();
        tomcat.setBaseDir("temp");
        tomcat.setPort(1024);
         
        StandardContext ctx = (StandardContext) tomcat.addWebapp(contextPath,
                new File(webappDir).getAbsolutePath());

        //declare an alternate location for your "WEB-INF/classes" dir:     
        File additionWebInfClasses = new File("target/classes");
        WebResourceRoot resources = new StandardRoot(ctx);
        resources.addPreResources(new DirResourceSet(resources, "/WEB-INF/classes", additionWebInfClasses.getAbsolutePath(), "/"));
        ctx.setResources(resources);

        tomcat.start();
        tomcat.getServer().await();    
    }
}