DUMMY_CodeQL_BODY= """{Id}. {Title}
   File: {File}
   Line: {Line}
   Code Snippet:
   ```{Snippet}```
"""

DUMMY_CodeQL_HEADER = """Dummy CodeQL Analysis Report
======================

Repository: {repo}
Branch: {branch}
Language: "python"

Results:


"""


SNIPPET = {
    "Python":"""python
   num = input("Enter a number: ")
   os.system("factorial_calc " + num)""",

   "NodeJS": """const readline = require('readline');
const { exec } = require('child_process');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("Enter a number: ", (num) => {
    exec("node factorial_calc.js " + num, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
        } else {
            console.log(stdout);
        }
        rl.close();
    });
});
""",

    "Java": """import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));

        System.out.print("Enter a number: ");
        String num = reader.readLine();
""",

    "CPP":"""#include <iostream>
#include <cstdlib>
using namespace std;

int main() {
    string num;
    cout << "Enter a number: ";
    getline(cin, num);""",
   }

BODY_CONTENT = [{
    "Id":"1",
"Title": "Potential Command Injection (Critical)",
"File": "dummy",
"Line": "15",
"Snippet": "{Snippet}",


},
{
"title": "Potential SSTI (high)",
},
]

