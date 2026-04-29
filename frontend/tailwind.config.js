/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          light: '#fdfcf0',
          DEFAULT: '#f3e8ff',
          dark: '#581c87',
        }
      }
    },
  },
  plugins: [],
}
