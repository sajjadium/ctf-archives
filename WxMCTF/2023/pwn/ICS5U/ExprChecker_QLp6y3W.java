import java.io.*;
import java.lang.reflect.*;
import java.net.*;
import java.util.*;
import javax.tools.*;

public class ExprChecker {

    private static void writeFile(String expr) {
        try {
            FileWriter writer = new FileWriter("./Helper.java");
            writer.write("public class Helper {\n");
            writer.write("    public static int checksum = 1337;\n");
            writer.write("    public static Object eval() {\n");
            writer.write("        return (Object) (" + expr + ");\n");
            writer.write("    }\n");
            writer.write("}\n");
            writer.close();
        } catch(IOException e) {}
    }

    private static boolean check(String expr) {
        writeFile(expr);
        try {
            // https://stackoverflow.com/a/21544850
            DiagnosticCollector<JavaFileObject> diagnostics = new DiagnosticCollector<JavaFileObject>();
            JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
            StandardJavaFileManager fileManager = compiler.getStandardFileManager(diagnostics, null, null);
            Iterable<? extends JavaFileObject> compilationUnit = fileManager.getJavaFileObjectsFromFiles(Arrays.asList(new File("Helper.java")));
            JavaCompiler.CompilationTask task = compiler.getTask(null, fileManager, diagnostics, new ArrayList(), null, compilationUnit);
            fileManager.close();
            // check 1: program compiles
            if(task.call()) {
                URLClassLoader classLoader = new URLClassLoader(new URL[] {new File("./").toURI().toURL()});
                Class helper = classLoader.loadClass("Helper");
                // check 2: checksum was unchanged (to protect against cosmic rays)
                Field f = helper.getField("checksum");
                return (Integer) f.get(null) == 1337;
            } else {
                // debug information upon compile failure
                for(Diagnostic<? extends JavaFileObject> diagnostic : diagnostics.getDiagnostics()) {
                    System.out.printf("Error on line %d: %s\n", diagnostic.getLineNumber(), diagnostic.getMessage(null));
                }
                return false;
            }
        } catch(Exception e) {
            return false;
        }
    }

    public static void main(String[] args) {
        System.out.println("This program will check whether a string you enter is a valid Java expression.");
        System.out.println("For example, \"a\" + 3 + (4 / 5) and new Object() are valid expressions.");
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        System.out.print("Enter a string: ");
        try {
            String expr = reader.readLine();
            if(check(expr)) {
                System.out.println("You entered a valid expression.");
            } else {
                System.out.println("You entered an invalid expression.");
            }
        } catch(IOException e) {}
    }
}
