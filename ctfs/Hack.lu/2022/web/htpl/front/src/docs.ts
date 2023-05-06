/*
 * Generate the documentation
 * This is not part of the challenge.
 */

import { ASTConstructor, registeredNodes } from "./ast";
import "./style/main.scss";

function createElement(tag: string, attrs: Record<string, any> = {}) {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    el.setAttribute(key, value);
  }
  Object.assign(el, attrs);
  return el;
}

function createDefinition(node: ASTConstructor) {
  const def = createElement("div", {
    class: "definition",
    id: node.nodeName,
  });

  if (node.documentation.description) {
    def.appendChild(
      createElement("div", {
        class: "description",
        textContent: node.documentation.description,
      })
    );
  }

  if (node.children && node.children.length) {
    const ul = createElement("ul", { class: "children" });
    for (const child of node.children) {
      const li = createElement("li", {});
      const suffix = child.many ? "..." : child.optional ? "?" : "";
      li.appendChild(document.createTextNode(`${child.name}${suffix}`));
      li.appendChild(
        createElement("a", {
          href: `#${child.type.nodeName}`,
          textContent: `(${child.type.nodeName})`,
        })
      );
      ul.appendChild(li);
    }
    def.appendChild(ul);
  }

  if (node.__proto__?.nodeName) {
    const el = createElement("div", { class: "parent" });
    const parent = node.__proto__;
    el.appendChild(
      createElement("a", {
        href: `#${parent.nodeName}`,
        textContent: parent.nodeName,
      })
    );
    def.appendChild(el);
  }

  const subclasses = getSubclasses(node);
  if (subclasses && subclasses.length) {
    const el = createElement("div", { class: "subclasses" });
    for (const cls of subclasses) {
      el.appendChild(
        createElement("a", {
          href: `#${cls.nodeName}`,
          textContent: cls.nodeName,
        })
      );
    }
    def.appendChild(el);
  }

  if (node.documentation.example) {
    const el = createElement("div", { class: "example" });
    el.textContent = node.documentation.example;
    def.appendChild(el);
  }

  document.querySelector("#doc")?.appendChild(def);
}

for (const node of registeredNodes) {
  createDefinition(node);
}

function getSubclasses(node: ASTConstructor) {
  const subs = [];
  for (const n of registeredNodes) {
    if (n.__proto__?.nodeName == node.nodeName) {
      subs.push(n);
    }
  }
  return subs;
}

window.addEventListener("hashchange", () => {
  const id = window.location.hash.slice(1);
  const el = document.querySelector(`#${id}`);
  if (el) {
    el.scrollIntoView();
  }
});
