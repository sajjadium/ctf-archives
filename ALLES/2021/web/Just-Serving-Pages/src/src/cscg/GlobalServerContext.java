package cscg;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

import javax.servlet.ServletContextEvent;  
import javax.servlet.ServletContextListener;
import cscg.user.*;
import java.util.UUID;

public class GlobalServerContext implements ServletContextListener {  

    @Override
    public void contextInitialized(ServletContextEvent servletContextEvent) {
        System.out.println("Starting up CSCG instance!");

        ArrayList<User> users = new ArrayList<User>();
        users.add(new User(1, "admin", UUID.randomUUID().toString(), true));

        servletContextEvent.getServletContext().setAttribute("users", users);

        // Read flag from system
        try (Scanner scanner = new Scanner( new File("/flag"), "ASCII" )) {
            String FLAG = scanner.useDelimiter("\\A").next();
            servletContextEvent.getServletContext().setAttribute("FLAG", FLAG);
        }
        catch (IOException e) {
            
        }

    }

    @Override
    public void contextDestroyed(ServletContextEvent servletContextEvent) {
        System.out.println("Shutting down!");
    }
}