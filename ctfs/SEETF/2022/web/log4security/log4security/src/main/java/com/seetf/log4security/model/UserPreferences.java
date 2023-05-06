package com.seetf.log4security.model;

import org.springframework.stereotype.Component;
import org.springframework.context.annotation.Scope;
import org.springframework.context.annotation.ScopedProxyMode;

import java.util.UUID;
import java.util.logging.Logger;
import java.util.logging.FileHandler;
import java.util.logging.Handler;
import java.util.logging.SimpleFormatter;

import java.io.File;

@Component
@Scope(value = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class UserPreferences {
    private String name = "User";
    private String location = "World";
    private Boolean logging = false;
    private Logger logger = null;
    private final String uuid = UUID.randomUUID().toString();

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getLocation() {
        return location;
    }

    public String setLocation(String location) {
        this.location = location;
        return location;
    }

    public String getUuid() {
        return uuid;
    }

    public Boolean getLogging() {
        return logging;
    }

    public Logger getLogger() {
        return logger;
    }

    private void resetLogger() {
        this.logger = Logger.getLogger(uuid);

        // Remove all handlers
        Handler[] handlers = this.logger.getHandlers();
        for (Handler handler : handlers) {
            handler.close();
            this.logger.removeHandler(handler);
        }

        // Delete log file
        String filename = "/tmp/" + this.getUuid() + "/access.log";
        File logFile = new File(filename);

        if (logFile.exists()) {
            logFile.delete();
        }

        try {
            // Create new log file and handler
            logFile.getParentFile().mkdirs();
            logFile.createNewFile();

            FileHandler fh = new FileHandler(filename);
            fh.setFormatter(new SimpleFormatter());
            this.logger.addHandler(fh);
        }
        catch (Exception e) {
            System.out.println("Error creating log file: " + filename);
            System.out.println(e.getMessage());
        }
    }

    public void setLogging(Boolean logging) {
        this.logging = logging;
        if (this.logging == true) {
            this.resetLogger();
        }
        else {
            this.logger = null;
        }
    }
}