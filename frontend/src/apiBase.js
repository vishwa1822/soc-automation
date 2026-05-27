/** Single backend origin for all dashboard API calls (override with Vite env). */
export const API_BASE = (import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000").replace(/\/$/, "")
