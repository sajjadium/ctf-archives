package cscg.user;

public class UserConfig {

    private boolean debugMode;
    private int language;
    private User user;

    public UserConfig() {
        this.debugMode = false;
        this.language = 0;
        this.user = null;
    }
    
    public boolean isDebugMode() {
        return debugMode;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public int getLanguage() {
        return language;
    }

    public void setLanguage(int language) {
        this.language = language;
    }

    public void setDebugMode(boolean debugMode) {
        this.debugMode = debugMode;
    }
}