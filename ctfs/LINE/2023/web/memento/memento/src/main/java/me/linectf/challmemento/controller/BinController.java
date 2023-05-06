package me.linectf.challmemento.controller;

import me.linectf.challmemento.context.AuthContext;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.net.MalformedURLException;
import java.net.URL;
import java.net.http.*;
import java.net.URI;
import java.util.*;

@Controller
@RequestMapping("/bin")
public class BinController {
    private static Map<String, List> userToBins = new HashMap<String, List>();
    private static Map<String, String> idToBin = new HashMap<String, String>();

    @Autowired
    private AuthContext authContext;

    @GetMapping("/{id}")
    public String bin(@PathVariable String id, Model model) {
        String bin = idToBin.get(id);
        model.addAttribute("bin", bin);
        return "bin";
    }

    @GetMapping("/list")
    public String binList(Model model) {
        if (authContext.userid.get() == null) return "redirect:/";
        model.addAttribute("bins", userToBins.get(authContext.userid.get()));
        return "list";
    }

    @GetMapping("/create")
    public String createForm() {
        return "create";
    }

    @PostMapping("/create")
    public String create(@RequestParam String bin) {
        String id = UUID.randomUUID().toString();
        if (userToBins.get(authContext.userid.get()) == null) {
            userToBins.put(authContext.userid.get(), new ArrayList<String>());
        }
        userToBins.get(authContext.userid.get()).add(id);
        idToBin.put(id, bin);
        return "redirect:/bin/" + id;
    }

    @RequestMapping("/report")
    public String report(@RequestParam String urlString) throws Exception {
        URL url = new URL(urlString);
        HttpClient.newHttpClient().send(HttpRequest.newBuilder(new URI("http://memento-admin:3000/?url=" + url.getPath())).build(), HttpResponse.BodyHandlers.ofString()).body();
        return "redirect:/" + url.getPath() + "#reported";
    }
}
