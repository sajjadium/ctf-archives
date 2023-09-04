package com.sekai.app.waf;


import lombok.Data;

@Data
public class WafViolation {
    private final AttackTypes attackType;
    private final String attackString;
}
