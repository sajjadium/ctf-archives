/*
* Self-serving hash browns machine.
* Run using Java 25.
* 
* © 2026 Shitty Systems Pty Ltd. No rights reserved (No one wants to use this crap, except you apparently). 
*/

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Scanner;

import java.io.*;
import java.nio.charset.StandardCharsets;

public class Main{

    static String WELCOME = """
    Welcome to the self-serving hash browns machine. 
    To get started, please enter a valid password.""";

    static Integer[] PERMITTED_HASHCODES = new Integer[] {
            982114681, -1367319387, 1329033977, 904090737, -862545276, -762593117, -110, 81925023, 5810259, -2959105,
            1029, 96320135, -29692049, 128
    };

    static boolean auth(Integer inputHash){
        for (Integer permittedHashcode : PERMITTED_HASHCODES) {
            if(permittedHashcode == inputHash){
                return true;
            }
        }
        return false;
    }

    public static void displayFlag() {
        try {
            String flag = Files.readString(Path.of("flag.txt"));
            System.out.println(flag);
        } catch (IOException e) {
            System.err.println("Could not read flag.txt");
        }
    }

    public static void main(String[] args){

        PrintWriter out = new PrintWriter(
            new OutputStreamWriter(System.out, StandardCharsets.UTF_8),
            true
        );

        out.println(WELCOME);
        out.print("> ");
        Scanner s = new Scanner(System.in);
        String input = s.nextLine();
        if(input.length() < 16){
            out.println("Passwords must be at least 16 characters long. But your input password is " + input.length() + " characters long.");
            System.exit(1);
        }
        if(auth(input.hashCode())){
            out.println("Authenticated! Here are your hash browns: \uD83E\uDD54\uD83E\uDD54\uD83E\uDD54");
            displayFlag();
        }else{
            out.println("Wrong password.");
            System.exit(1);
        }

    }
    
}
