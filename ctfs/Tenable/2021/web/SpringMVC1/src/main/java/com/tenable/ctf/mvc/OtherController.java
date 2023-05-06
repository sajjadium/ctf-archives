package com.tenable.ctf.mvc;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import javax.servlet.http.HttpSession;

@Controller
public class OtherController {

	@GetMapping("/other")
	public String index(@RequestParam(name="name", required=false, defaultValue="user") String realName, HttpSession session, Model model) {
		session.setAttribute("realName", realName);
		model.addAttribute("name", realName);
		return "hello";
	}

}
