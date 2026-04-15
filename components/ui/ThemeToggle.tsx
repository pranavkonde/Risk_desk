"use client";

import { useEffect, useState } from "react";

type Theme = "dark" | "light";

function applyTheme(theme: Theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme", theme);
}

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>("dark");
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("theme");
    const resolved: Theme = stored === "light" ? "light" : "dark";
    setTheme(resolved);
    applyTheme(resolved);
    setReady(true);
  }, []);

  const toggle = () => {
    const next: Theme = theme === "dark" ? "light" : "dark";
    setTheme(next);
    applyTheme(next);
  };

  return (
    <button className="theme-toggle" onClick={toggle} aria-label="Toggle theme" disabled={!ready}>
      {theme === "dark" ? "Light" : "Dark"}
    </button>
  );
}
