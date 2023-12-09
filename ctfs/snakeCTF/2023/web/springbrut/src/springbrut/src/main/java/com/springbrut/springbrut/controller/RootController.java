package com.springbrut.springbrut.controller;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RootController {
  @GetMapping("/")
  public ResponseEntity<String> notHere() {
    HttpHeaders headers = new HttpHeaders();
    headers.add("Location", "/auth/helloworld");
    return new ResponseEntity<String>(headers, HttpStatus.FOUND);
  }
}
