package com.linectf.safeNote.controller.rest;

import com.linectf.safeNote.controller.request.LoginRequest;
import com.linectf.safeNote.controller.request.RegisterRequest;
import com.linectf.safeNote.controller.response.LoginResponse;
import com.linectf.safeNote.controller.response.RegisterResponse;
import com.linectf.safeNote.controller.response.Response;
import com.linectf.safeNote.service.UserService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequestMapping("/api/user")
@RequiredArgsConstructor
public class UserRestController {
    private final UserService userService;

    @PostMapping("/register")
    public Response<RegisterResponse> register(@RequestBody RegisterRequest request) {

        return Response.success(
                RegisterResponse.fromUser(
                        userService.register(
                                request.getUsername(),
                                request.getPassword()
                        )
                )
        );
    }

    @PostMapping("/login")
    public Response<LoginResponse> login(@RequestBody LoginRequest request) {
        String token = userService.login(
                request.getUsername(),
                request.getPassword()
        );
        return Response.success(
                new LoginResponse(token)
        );
    }

    @GetMapping("/info")
    public Response<RegisterResponse> info(Authentication authentication) {
        return Response.success(
                RegisterResponse.fromUser(
                        userService.loadUserByUsername(
                                authentication.getName()
                        )
                )
        );
    }
}