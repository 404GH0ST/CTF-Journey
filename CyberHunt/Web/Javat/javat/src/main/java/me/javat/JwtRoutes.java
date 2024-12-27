package me.javat;

import io.jsonwebtoken.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletResponse;

import java.security.Key;
import java.security.KeyPair;

@Controller
public class JwtRoutes {
    public static final String ADMIN = "admin";
    public static final String REPL = "replican";
    public static final String GUEST = "guest";
    public static final String random = "random";
    public static final String FLAG = System.getenv("FLAG");
    KeyPair keyPair = Keys.keyPairFor(SignatureAlgorithm.ES256);

    @PostMapping("/login")
    public String login(@ModelAttribute("username") String username,
                        @ModelAttribute("password") String password,
                        HttpServletResponse response,
                        RedirectAttributes redirectAttributes) {
        String jwtToken = Jwts.builder().setSubject(GUEST).signWith(keyPair.getPrivate()).compact();
        Cookie cookie = new Cookie("auth", jwtToken);
        cookie.setMaxAge(3600); 
        cookie.setPath("/");
        response.addCookie(cookie);

        redirectAttributes.addAttribute("auth", "success");
        return "redirect:/";
    }
    
    @GetMapping("/")
    public String index(@RequestParam(required = false) String rpjwt, 
                        Model model,
                        @CookieValue(name = "auth", required = false) String jwtToken) {
        String sub = random;
        String jwt_guest = Jwts.builder().setSubject(GUEST).signWith(keyPair.getPrivate()).compact();
        if (rpjwt == null && jwtToken != null) {
            try {
                Jws<Claims> jwt = Jwts.parser().setSigningKey(keyPair.getPublic()).parseClaimsJws(jwtToken);
                Claims claims = (Claims) jwt.getBody();
                if (claims.getSubject().equals(ADMIN)) {
                    sub = ADMIN;
                } else if (claims.getSubject().equals(GUEST)) {
                    sub = GUEST;
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else if (rpjwt != null) {
            try {
                sub = REPL;
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        model.addAttribute("jwt", jwt_guest);
        model.addAttribute("sub", sub);
        if (sub.equals(ADMIN)) model.addAttribute("flag", FLAG);

        return "index";
    }

    
}
