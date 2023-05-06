package com.linectf.safeNote.controller.request;

import lombok.Getter;
import lombok.AllArgsConstructor;

@Getter
@AllArgsConstructor
public class RegisterRequest {
    private String username;
    private String password;
}
