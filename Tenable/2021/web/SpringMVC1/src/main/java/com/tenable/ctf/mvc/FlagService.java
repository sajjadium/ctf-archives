package com.tenable.ctf.mvc;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import com.tenable.ctf.mvc.Flag;
import org.springframework.stereotype.Component;

@Component
public class FlagService {
	private ApplicationContext context;
	public FlagService() {
		this.context = new ClassPathXmlApplicationContext("beans.xml");
	}

	public String getFlag(String flagName) {
		String value = "";
		try {
			Flag flag = (Flag) this.context.getBean(flagName);
			value = flag.getFlag();
		} catch (Exception e) {
			value = "Error getting flag!";
		}
		return value;
	}
}
