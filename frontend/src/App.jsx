import { useState } from "react";

const riskColors = {
  HIGH: "#ff4d4f",
  WARNING: "#faad14",
  SAFE: "#22c55e",
};

const alertText = {
  HIGH: "🚨 HIGH RISK: Immediate collision threat detected",
  WARNING: "⚠️ WARNING: Close approach detected",
  SAFE: "✅ SAFE: No significant collision risk",
};

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [hours, setHours] = useState(24);
  const [step, setStep] = useState(10);

  const fetchPrediction = async () => {
    setLoading(true);
    const res = await fetch(
      `http://127.0.0.1:8000/predict?hours=${hours}&step=${step}`
    );
    const json = await res.json();
    setData(json);
    setLoading(false);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100vw",
        background: "radial-gradient(circle at top, #0f172a, #020617)",
        color: "#e5e7eb",
        padding: "32px",
        fontFamily: "Inter, Arial, sans-serif",
      }}
    >
      {/* Header */}
      <h1 style={{ fontSize: "36px", marginBottom: "6px" }}>
        🛰️ Space Debris Collision Predictor
      </h1>
      <p style={{ color: "#94a3b8", marginBottom: "20px" }}>
        Physics-based satellite collision risk analysis
      </p>

      {/* Alert Banner */}
      {data && (
        <div
          style={{
            background: riskColors[data.most_dangerous_debris.risk_level],
            color: "#020617",
            padding: "16px 20px",
            borderRadius: "12px",
            fontWeight: "600",
            marginBottom: "24px",
            maxWidth: "900px",
          }}
        >
          {alertText[data.most_dangerous_debris.risk_level]}
        </div>
      )}

      {/* Main Grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "24px",
        }}
      >
        {/* LEFT COLUMN */}
        <div>
          {/* Controls */}
          <div
            style={{
              background: "#020617",
              border: "1px solid #1e293b",
              borderRadius: "14px",
              padding: "24px",
              marginBottom: "20px",
            }}
          >
            <div style={{ marginBottom: "20px" }}>
              <label>
                Prediction Window: <b>{hours} hours</b>
              </label>
              <input
                type="range"
                min="1"
                max="72"
                value={hours}
                onChange={(e) => setHours(e.target.value)}
                style={{ width: "100%" }}
              />
            </div>

            <div>
              <label>
                Time Step: <b>{step} minutes</b>
              </label>
              <input
                type="range"
                min="1"
                max="60"
                value={step}
                onChange={(e) => setStep(e.target.value)}
                style={{ width: "100%" }}
              />
            </div>
          </div>

          {/* Button */}
          <button
            onClick={fetchPrediction}
            style={{
              width: "100%",
              background: "#2563eb",
              border: "none",
              padding: "16px",
              borderRadius: "12px",
              color: "white",
              fontSize: "18px",
              fontWeight: "600",
              cursor: "pointer",
            }}
          >
            {loading ? "Running Prediction…" : "Run Prediction"}
          </button>
        </div>

        {/* RIGHT COLUMN */}
        {data && (
          <div
            style={{
              background: "#020617",
              border: "1px solid #1e293b",
              borderRadius: "14px",
              padding: "28px",
            }}
          >
            <h2 style={{ marginBottom: "16px" }}>
              Satellite: {data.satellite}
            </h2>

            <div style={{ lineHeight: "2" }}>
              <p>
                <b>Most Dangerous Debris:</b>{" "}
                {data.most_dangerous_debris.debris}
              </p>
              <p>
                <b>Closest Distance:</b>{" "}
                {data.most_dangerous_debris.min_distance_km} km
              </p>
              <p>
                <b>Collision Probability:</b>{" "}
                {data.most_dangerous_debris.collision_probability}
              </p>
              <p>
                <b>Time (UTC):</b>{" "}
                {data.most_dangerous_debris.time_utc}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
