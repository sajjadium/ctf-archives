const CUSTOM_KEY = "__custom__";
const CUSTOM_TYPES = [
  "Object",
  "String",
  "Boolean",
  "Array",
  "Function",
  "RegExp",
];

type Dict = Record<string, unknown>;
type Custom = {
  [CUSTOM_KEY]: true;
  type: string;
  args: unknown[];
};

const isDict = (value: unknown): value is Dict => {
  return value === Object(value);
};

const isCustom = (value: unknown): value is Custom => {
  return isDict(value) && !!value[CUSTOM_KEY];
};

const set = (target: unknown, key: string, value: unknown) => {
  if (!isDict(target)) return;
  if (key in target) return;
  target[key] = value;
};

const merge = (target: unknown, input: Dict) => {
  if (!isDict(target)) return;
  for (const key of Object.keys(input)) {
    const value = input[key];
    if (!isDict(value)) {
      set(target, key, value);
    } else if (Array.isArray(value)) {
      set(target, key, []);
      merge(target[key], value);
    } else if (!isCustom(value)) {
      set(target, key, {});
      merge(target[key], value);
    } else {
      const { type, args } = value;
      if (CUSTOM_TYPES.includes(type)) {
        try {
          set(target, key, new globalThis[type](...args));
        } catch {}
      }
    }
  }
};

const inputStr = prompt("Input your JSON:") ?? "";

const target: Dict = {
  title: "deno-ppjail",
  category: "sandbox",
};
merge(target, JSON.parse(inputStr));
