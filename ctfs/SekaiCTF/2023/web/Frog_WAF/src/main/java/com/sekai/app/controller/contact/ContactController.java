package com.sekai.app.controller.contact;

import lombok.val;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpSession;
import javax.validation.Valid;
import java.util.ArrayList;

@RestController
class ContactController {

    private final static String CONTACTS = "contacts";

    @PostMapping("/addContact")
    ResponseEntity<String> addContact(HttpSession session, @Valid @RequestBody Contact contact) {
        if (session.getAttribute(CONTACTS) == null) {
            session.setAttribute(CONTACTS, new ArrayList<Contact>());
        }
        val contacts = (ArrayList<Contact>) session.getAttribute(CONTACTS);
        contacts.add(contact);
        return ResponseEntity.ok("contact added");
    }

    @GetMapping("/")
    ModelAndView index(HttpSession session) {
        if (session.getAttribute(CONTACTS) == null) {
            session.setAttribute(CONTACTS, new ArrayList<Contact>());
        }
        val modelAndView = new ModelAndView("index.html");
        val contacts = (ArrayList<Contact>) session.getAttribute(CONTACTS);
        modelAndView.addObject("contacts", contacts);
        return modelAndView;
    }

}
