const defaultTheme = require("tailwindcss/defaultTheme");

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.tsx",
    "node_modules/flowbite-react/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Noto Sans Cypro Minoan", defaultTheme.fontFamily.sans],
        serif: ["Unna", ...defaultTheme.fontFamily.serif],
      },
    },
  },
  plugins: [require("flowbite/plugin")],
};
