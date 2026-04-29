/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: '#1A1A1A',
          surface: '#242424',
          elevated: '#2E2E2E',
        },
        text: {
          primary: '#E8E0D8',
          secondary: '#A09888',
        },
        accent: {
          primary: '#C87533',
          secondary: '#8B6914',
        },
        border: '#3A3A3A',
        success: '#4A7C59',
        danger: '#8B3A3A',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Lora', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
