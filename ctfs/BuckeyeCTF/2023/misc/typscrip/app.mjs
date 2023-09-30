import { createServer } from "net";
import { Project } from "ts-morph";

const flag = process.env.FLAG ?? "bctf{fake_flag}";

function compile(source) {
    const project = new Project({ useInMemoryFileSystem: true });
    const sourceFile = project.createSourceFile("temp.ts", source);
    const diagnostics = sourceFile.getPreEmitDiagnostics();

    return diagnostics.map(diagnostic => {
        const severity = ["Warning", "Error", "Suggestion", "Message"][diagnostic.getCategory()];
        return `${severity} on line ${diagnostic.getLineNumber()}`;
    });
}

const server = createServer(socket => {
    socket.write("What is your name?\n> ");
    socket.once("data", data => {
        const name = data.toString().trim();
        socket.write(`Hello, ${name}. Give me some code: (end with blank line)\n> `);
        let code = '';
        let done = false;
        socket.on('data', data => {
            if (done) return;
            const line = data.toString().trim();
            if (!line) {
                done = true;
                socket.write('Thinking...\n');

                const today = new Date().toLocaleDateString('en-us');
                const source = `/* TYPE CHECKED FOR ${name} ON ${today}. THE FLAG IS "${flag}". */` + "\n\n" + code;

                const errors = compile(source);

                if (errors.length === 0) {
                    socket.write('Congrats, your code is perfect\n');
                } else {
                    socket.write(errors.join('\n') + '\n');
                }

                socket.destroy();
            }
            if (!done) socket.write('> ');

            code += line + '\n';
        })
    });
});

server.listen(1024);
