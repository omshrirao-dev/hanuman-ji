/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0D0D0F",
        card: "#141419",
        saffron: "#FF8C1A",
        rose: "#C9758E",
        warmwhite: "#F5F0E8",
        muted: "#8D8473",
      },
      fontFamily: {
        ui: ["Inter", "sans-serif"],
        devanagari: ["Noto Sans Devanagari", "sans-serif"],
      },
      keyframes: {
        "pulse-ring": {
          "0%": { boxShadow: "0 0 0 0 rgba(255, 140, 26, 0.5)" },
          "70%": { boxShadow: "0 0 0 14px rgba(255, 140, 26, 0)" },
          "100%": { boxShadow: "0 0 0 0 rgba(255, 140, 26, 0)" },
        },
      },
      animation: {
        "pulse-ring": "pulse-ring 1.6s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
    },
  },
  plugins: [],
};
