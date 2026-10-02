/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        fintech: {
          blue: '#0052FF',
          'blue-hover': '#0045D8',
          'blue-light': '#EBF2FF',
          black: '#08090C',
          charcoal: '#1A1D24',
          muted: '#64748B',
          paper: '#F8F9FA',
          paperdark: '#F1F3F5',
          border: '#08090C',
          gray: '#E2E8F0',
        }
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        sans: ['Inter', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        'brutal': '4px 4px 0px 0px #08090C',
        'brutal-sm': '2px 2px 0px 0px #08090C',
        'brutal-lg': '6px 6px 0px 0px #08090C',
        'brutal-xl': '8px 8px 0px 0px #08090C',
        'brutal-white': '4px 4px 0px 0px #FFFFFF',
        'brutal-blue': '4px 4px 0px 0px #0052FF',
      },
      letterSpacing: {
        'tightest': '-0.04em',
        'tighter': '-0.03em',
        'tight': '-0.02em',
      }
    },
  },
  plugins: [],
}
