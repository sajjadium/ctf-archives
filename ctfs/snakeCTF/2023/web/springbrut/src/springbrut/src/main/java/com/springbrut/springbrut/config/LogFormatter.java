package com.springbrut.springbrut.config;

import java.util.Map;
import java.util.stream.Collectors;
import org.zalando.logbook.HttpHeaders;
import org.zalando.logbook.StructuredHttpLogFormatter;

public class LogFormatter implements StructuredHttpLogFormatter {

    @Override
    public String format(final Map<String, Object> content) {
        if(content.entrySet().stream().anyMatch(x -> x.getKey().equals("origin") && x.getValue().equals("local")))
            return "";
        return "Request: ".concat(content.entrySet().stream()
                .map(entry ->{                     
                    if (entry.getKey().equals("headers")) {
                        HttpHeaders headers = (HttpHeaders)entry.getValue();
                        if (headers.containsKey("X-Original-Ip"))
                            return String.format("IP: %s,", headers.getFirst("X-Original-Ip"));
                    }
                    if (entry.getKey().equals("uri"))
                        return String.format("URI: %s,", entry.getValue().toString());
                    if (entry.getKey().equals("method"))
                        return String.format("METHOD: %s,", entry.getValue().toString());

                    return "";
                })
                .collect(Collectors.joining(" ")));
    }

}
