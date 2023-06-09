package org.intrigus.ctf.gpnctf23;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

import org.apache.commons.jxpath.JXPathContext;

public class Main {

	public static void main(String[] args) {
		System.out.println("Give me an XPath expression:");
		String str;
		try {
			str = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8)).readLine();
			str = str.replace(".", "/"); // <--
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("Failed to read your XPath expression.");
			return;
		}
		try {
			JXPathContext context = JXPathContext.newContext(new Object());
			System.out.println(context.getValue(str));
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Failed to get the value of your XPath expression.");
			return;
		}
	}

}
