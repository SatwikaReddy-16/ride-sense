const API_BASE_URL = "http://127.0.0.1:8000";

// --------------------
// Predict single month
// --------------------
export async function fetchPrediction(year, month, signal) {
  try {
    const res = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ year, month }),
      signal,
    });

    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`API ${res.status}: ${txt}`);
    }

    return await res.json();
  } catch (err) {
    if (err.name === "AbortError") {
      return { error: true, aborted: true };
    }
    console.error("API error (predict):", err);
    return { error: true };
  }
}

// --------------------
// Predict future series
// --------------------
export async function fetchHistory(year, month, signal) {
  try {
    const res = await fetch(`${API_BASE_URL}/predict_series`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ year, month }),
      signal,
    });

    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`API ${res.status}: ${txt}`);
    }

    return await res.json(); // { history: [...] }
  } catch (err) {
    if (err.name === "AbortError") {
      return { history: [] };
    }
    console.error("API error (history):", err);
    return { history: [] };
  }
}
