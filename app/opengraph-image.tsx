import { ImageResponse } from "next/og";

export const runtime = "edge";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default function OGImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: 48,
          background:
            "radial-gradient(1200px 700px at 10% -20%, #1a3872 0%, transparent 55%), linear-gradient(180deg, #0d1730, #070c18)",
          color: "#f3f7ff",
          fontFamily: "Inter, sans-serif",
        }}
      >
        <div style={{ fontSize: 24, letterSpacing: 1.2, textTransform: "uppercase", color: "#a3c9ff" }}>
          Pacifica Risk Desk
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <div style={{ fontSize: 68, fontWeight: 700, lineHeight: 1.05, maxWidth: 980 }}>
            Institutional-grade analytics for Pacifica traders
          </div>
          <div style={{ fontSize: 28, color: "#9fb0d3", maxWidth: 980 }}>
            Funding radar, execution analytics, and portfolio risk monitoring.
          </div>
        </div>
        <div style={{ display: "flex", gap: 14 }}>
          {["Funding", "Execution", "Risk", "Testnet/Mainnet"].map((x) => (
            <div
              key={x}
              style={{
                border: "1px solid rgba(140,180,255,0.35)",
                borderRadius: 999,
                padding: "8px 16px",
                fontSize: 20,
                color: "#b9d4ff",
                background: "rgba(11,18,36,0.7)",
              }}
            >
              {x}
            </div>
          ))}
        </div>
      </div>
    ),
    {
      ...size,
    },
  );
}
