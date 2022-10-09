// @ts-nocheck
import { parse } from "qs";

const buildDefaultSettings = () => {
  const meta = Object.create(null, {
    robots: { value: "noindex nofollow" },
    description: { value: "Just a simple todo app" },
    keywords: { value: "Svelte" },
  });
  return { title: "Yatodo", meta };
};

const parseQueryString = (query) =>
  parse(query, {
    ignoreQueryPrefix: true,
    allowPrototypes: true,
    depth: 1,
  });

const cleanStr = (str) => decodeURI(str).replaceAll(/[,"{}]/g, "");

const generateTemplate = (arr) =>
  Array.isArray(arr) &&
  `{"${arr[0]}": {"${arr[1]}": {"${arr[2]}":"${arr[3]}" }}}`;

const extractSettings = ({ settings }) => {
  if (settings instanceof Array && !Array.isArray(settings)) {
    return generateTemplate(settings.map((setting) => cleanStr(setting)));
  }
  return JSON.stringify({});
};

const combineSettings = (defaultsSettings, userSettings) => {
  Object.keys(userSettings).forEach((key) => {
    if (typeof userSettings[key] === "object") {
      defaultsSettings[key] = combineSettings(
        defaultsSettings[key] || Object.create(null),
        userSettings[key]
      );
    } else {
      defaultsSettings[key] = userSettings[key];
    }
  });
  return defaultsSettings;
};

export {
  buildDefaultSettings,
  parseQueryString,
  combineSettings,
  extractSettings,
};
