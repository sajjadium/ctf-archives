/**
 *  Create monaco editor and add auto completion for custom nodes
 *
 *  This is not part of the challenge, but feel free to use a monaco 0day :D
 */

export async function createEditor(container: HTMLElement, code: string = "") {
  const monaco = await import("monaco-editor");

  type OnChangeCallback = (code: string) => void;
  type OnRunCallback = () => void;

  const onChangeCallbacks: OnChangeCallback[] = [];
  const onRunCallbacks: OnRunCallback[] = [];

  const editor = monaco.editor.create(container, {
    language: "python",
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
