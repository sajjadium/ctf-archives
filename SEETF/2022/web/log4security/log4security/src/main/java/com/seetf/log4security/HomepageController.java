package com.seetf.log4security;

import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.charset.StandardCharsets;

import java.security.MessageDigest;
import org.apache.commons.codec.binary.Hex;

import com.seetf.log4security.model.UserPreferences;

@Controller
public class HomepageController {
	@Autowired private UserPreferences userPreferences;

	@GetMapping("/")
	public ModelAndView index(ModelMap model) {
		return new ModelAndView("redirect:/home", model);
	}

	@GetMapping("/home")
	public String home(@RequestHeader("User-Agent") String userAgent, Model model) {
		if (userPreferences.getLogging()) {
			userPreferences.getLogger().info("Visited by " + userAgent);
		}
		model.addAttribute("name", userPreferences.getName());
		model.addAttribute("location", userPreferences.getLocation());
		return "home";
	}

	@GetMapping("/logs")
	public String auth(Model model) {
		return "auth";
	}

	@PostMapping("/logs")
	public String logs(@RequestParam("token") String token, Model model) {

		MessageDigest digestStorage;
		try {
			digestStorage = MessageDigest.getInstance("SHA-1");
			digestStorage.update(System.getenv("SUPER_SECRET").getBytes("ascii"));	
		}
		catch (Exception e) {
			model.addAttribute("logs", "Error getting secret token, please contact CTF admins.");
			return "logs";
		}

		if (userPreferences.getLogging()) {
			userPreferences.getLogger().info("Logging in with token " + token);

			// Log login attempt
			String correctToken = new String(Hex.encodeHex(digestStorage.digest()));
			userPreferences.getLogger().info("Login attempt with token " + token + "=" + correctToken);
		}

		// Invalid token
		if (!token.equals(new String(Hex.encodeHex(digestStorage.digest())))) {
			model.addAttribute("logs", "Invalid token");
			return "logs";
		}

		if (userPreferences.getLogging()) {
			try {
				String filename = "/tmp/" + userPreferences.getUuid() + "/access.log";
				Path filePath = Paths.get(filename);
				model.addAttribute("logs", Files.readString(filePath, StandardCharsets.US_ASCII));
			}
			catch (Exception e) {
				System.out.println("Error reading log file: " + e.getMessage());
				model.addAttribute("logs", "Error reading logs");
			}
		}
		else {
			model.addAttribute("logs", "Logging is disabled");
		}
		return "logs";
	}

	@PostMapping("/api/preferences")
	@ResponseBody
	public String preferences(@RequestBody UserPreferences preferences) {
		try {
			userPreferences.setName(preferences.getName());
			userPreferences.setLocation(preferences.getLocation());
			userPreferences.setLogging(preferences.getLogging());
			return "OK";
		} catch (Exception e) {
			return "ERROR";
		}
	}
}