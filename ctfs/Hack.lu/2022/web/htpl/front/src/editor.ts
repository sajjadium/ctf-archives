import { registeredNodes } from "./ast/AST";

/**
 *  Create monaco editor and add auto completion for custom nodes
 *
 *  This is not part of the challenge, but feel free to use a monaco 0day :D
 */

export async function createEditor(container: HTMLElement, code: string = "") {
  const monaco = await import("monaco-editor");

  type OnChangeCallback = (code: string) => void;
  type OnRunCallback = () => void;

  function addNodeCompletion() {
    monaco.languages.registerCompletionItemProvider("html", {
      provideCompletionItems(model, position, _context, _token) {
        if (!model) {
          throw new Error("model is null");
        }

        const word = model.getWordUntilPosition(position);
        const range = {
          startLineNumber: position.lineNumber,
          endLineNumber: position.lineNumber,
          startColumn: word.startColumn,
          endColumn: word.endColumn,
        };
        const items = Array.from(registeredNodes).map((node) => ({
          label: `x-${node.nodeName}`,
          detail: node.documentation.description,
          kind: monaco.languages.CompletionItemKind.Property,
          insertText: `x-${node.nodeName}>$0</x-${node.nodeName}>`,
          insertTextRules:
            monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,

          range,
        }));
        return { suggestions: items };
      },
      triggerCharacters: ["<"],
    });
  }

  const onChangeCallbacks: OnChangeCallback[] = [];
  const onRunCallbacks: OnRunCallback[] = [];

  addNodeCompletion();
  const editor = monaco.editor.create(container, {
    language: "html",
    theme: "vs-dark",
    automaticLayout: true,
    value: code,
  });

  const model = editor.getModel();
  if (!model) {
    throw new Error("Could not get model");
  }

  model.onDidChangeContent(() => {
    const code = editor.getValue();
    onChangeCallbacks.forEach((cb) => cb(code));
  });
  editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
    onRunCallbacks.forEach((cb) => cb());
  });

  return {
    onChange(cb: OnChangeCallback) {
      onChangeCallbacks.push(cb);
    },
    onRun(cb: OnRunCallback) {
      onRunCallbacks.push(cb);
    },
  };
}
