package com.linectf.safeNote.controller.response;

import com.linectf.safeNote.model.User;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class RegisterResponse {

    private Integer id;
    private String username;

    public static RegisterResponse fromUser(User user) {
        return new RegisterResponse(
                user.getId(),
                user.getUsername()
        );
    }
}
