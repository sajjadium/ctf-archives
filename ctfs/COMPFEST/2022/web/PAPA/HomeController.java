package id.compfest.papa;

import id.compfest.papa.model.HomeModel;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class HomeController {
	private static final String FLAG = "COMPFEST14{**REDACTED**}";
	
    @GetMapping
    public String getHome(Model model) {
        model.addAttribute("homeModel", new HomeModel());
        return "home";
    }

    @PostMapping("/post")
    public String postHome(@ModelAttribute HomeModel home, Model model) {
		if(home.getSecret().equals(FLAG)) {
			return "win";
		}
        return "home";
    }
	
	@PutMapping("/put")
    public String putHome(@ModelAttribute HomeModel home, Model model) {
        return "home";
    }
	
	@DeleteMapping("/delete")
    public String deleteHome(@ModelAttribute HomeModel home, Model model) {
        return "home";
    }
}
