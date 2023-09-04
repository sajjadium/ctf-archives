package com.sekai.app.waf;

import lombok.Getter;

public enum AttackTypes {
    SQLI("\"", "'", "#"),
    XSS(">", "<"),
    OS_INJECTION("bash", "&", "|", ";", "`", "~", "*"),
    CODE_INJECTION("for", "while", "goto", "if"),
    JAVA_INJECTION("Runtime", "class", "java", "Name", "char", "Process", "cmd", "eval", "Char", "true", "false"),
    IDK("+", "-", "/", "*", "%", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9");

    @Getter
    private final String[] attackStrings;

    AttackTypes(String... attackStrings) {
        this.attackStrings = attackStrings;
    }

}
