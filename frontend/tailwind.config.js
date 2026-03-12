/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{svelte,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Outfit"', 'sans-serif'],
      },
      colors: {
        'brand': {
          DEFAULT: '#10b981', // emerald-500
          dark: '#047857',   // emerald-700
          light: '#34d399',  // emerald-400
        },
        'dark': {
          bg: '#000000',      // deeper black for premium feel
          surface: '#121212', // elevated surface
          card: '#1e1e1e',    // cards
          border: '#333333',  // subtle borders
        }
      },
      boxShadow: {
        'neon': '0 0 15px rgba(16, 185, 129, 0.5)',
      }
    },
  },
  plugins: [],
}
