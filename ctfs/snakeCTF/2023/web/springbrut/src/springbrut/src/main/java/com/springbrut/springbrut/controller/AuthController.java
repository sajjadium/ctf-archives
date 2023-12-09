package com.springbrut.springbrut.controller;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/auth")
public class AuthController {
  @GetMapping("/helloworld")
  public String salutavaSempre() {
    return "status";
  }

  @GetMapping("/flag")
  public ResponseEntity<String> flaggavaSempre() {
    File f = new File("/flag");
    String flag;
    try {
      InputStream in = new FileInputStream(f);
      flag = new String(in.readAllBytes());
      in.close();
    } catch (Exception e) {
      flag = "PLACEHOLDER";
    }
    return new ResponseEntity<String>(flag, HttpStatus.OK);
  }
}
