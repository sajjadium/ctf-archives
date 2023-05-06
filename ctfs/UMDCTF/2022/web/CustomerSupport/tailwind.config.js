module.exports = {
  content: [    "./pages/**/*.{js,ts,jsx,tsx}",    "./components/**/*.{js,ts,jsx,tsx}",  ],
  theme: {
    extend: {
      backgroundImage: {
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
