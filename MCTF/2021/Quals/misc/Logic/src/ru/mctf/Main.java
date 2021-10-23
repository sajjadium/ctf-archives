package ru.mctf;

import ru.mctf.parser.BooleanObject;
import ru.mctf.parser.Parser;

import java.io.File;
import java.io.IOException;
import java.util.Collections;
import java.util.List;

public class Main {

    public static void main(String[] args) throws IOException {
        File outFile = new File("result.bin");
        String equation = "((a and b) xor (c or d))";
        Parser parser = new Parser();

        final BooleanObject parsed = parser.parse(equation);
        if (!equation.equals(parsed.toString())) {
            System.out.println("Failed to parse");
            return;
        }

        int id = 1;
        List<BooleanObject> objects = parser.getAllObjects();
        for (BooleanObject object : objects) {
            object.setId(id++);
        }

        Collections.shuffle(objects);
        BinaryFormatWriter.write(objects, outFile);
        System.out.println("Done!");
    }

}
