import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#07080A",
        panel: "#101216",
        panel2: "#161A20",
        silver: "#C0C0C0",
        steel: "#8E99A8",
        line: "#2A2F38",
        success: "#62D394"
      },
      boxShadow: {
        silver: "0 0 0 1px rgba(192,192,192,.22), 0 18px 60px rgba(0,0,0,.35)"
      }
    }
  },
  plugins: []
};

export default config;
