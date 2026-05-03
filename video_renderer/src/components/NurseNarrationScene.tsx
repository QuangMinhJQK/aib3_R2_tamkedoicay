import { AbsoluteFill } from "remotion";

type NurseNarrationSceneProps = {
  title: string;
  narration: string;
  accentColor: string;
  background: string;
  panel?: React.ReactNode;
};

const NurseAvatar: React.FC<{ accentColor: string }> = ({ accentColor }) => {
  return (
    <div style={{ position: "relative", width: 340, height: 520, flexShrink: 0 }}>
      <div
        style={{
          position: "absolute",
          left: 75,
          top: 54,
          width: 170,
          height: 170,
          borderRadius: "50%",
          background: "linear-gradient(180deg, #ffe8cf 0%, #f4c8a0 100%)",
          boxShadow: "0 18px 40px rgba(56, 76, 108, 0.18)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 58,
          top: 38,
          width: 204,
          height: 58,
          borderRadius: 40,
          background: "linear-gradient(180deg, #7fd0ff 0%, #3fa8ff 100%)",
          transform: "rotate(-4deg)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 96,
          top: 78,
          width: 126,
          height: 126,
          borderRadius: "50%",
          background: "#fff7f0",
        }}
      />
      <div style={{ position: "absolute", left: 132, top: 128, width: 10, height: 10, borderRadius: "50%", background: "#213547" }} />
      <div style={{ position: "absolute", left: 178, top: 128, width: 10, height: 10, borderRadius: "50%", background: "#213547" }} />
      <div
        style={{
          position: "absolute",
          left: 149,
          top: 154,
          width: 26,
          height: 14,
          borderBottom: "4px solid #e67e8a",
          borderRadius: "0 0 26px 26px",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 90,
          top: 176,
          width: 160,
          height: 220,
          borderRadius: 36,
          background: "linear-gradient(180deg, #f4fbff 0%, #d4f0ff 100%)",
          boxShadow: "0 22px 50px rgba(56, 76, 108, 0.12)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 42,
          top: 218,
          width: 90,
          height: 26,
          borderRadius: 20,
          background: "linear-gradient(180deg, #f4fbff 0%, #d4f0ff 100%)",
          transform: "rotate(-18deg)",
        }}
      />
      <div
        style={{
          position: "absolute",
          right: 42,
          top: 218,
          width: 90,
          height: 26,
          borderRadius: 20,
          background: "linear-gradient(180deg, #f4fbff 0%, #d4f0ff 100%)",
          transform: "rotate(18deg)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 126,
          top: 256,
          width: 54,
          height: 54,
          borderRadius: "50%",
          background: "linear-gradient(180deg, #7fd0ff 0%, #3fa8ff 100%)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "white",
          fontSize: 30,
          fontWeight: 700,
        }}
      >
        +
      </div>
      <div
        style={{
          position: "absolute",
          left: 110,
          top: 380,
          width: 120,
          height: 118,
          borderRadius: 28,
          background: "linear-gradient(180deg, #7fd0ff 0%, #3fa8ff 100%)",
          boxShadow: "0 20px 40px rgba(63, 168, 255, 0.28)",
        }}
      />
      <div style={{ position: "absolute", left: 128, top: 412, width: 84, height: 8, borderRadius: 8, background: "#ffffff" }} />
      <div style={{ position: "absolute", left: 128, top: 432, width: 84, height: 8, borderRadius: 8, background: "#ffffff" }} />
      <div style={{ position: "absolute", left: 128, top: 452, width: 84, height: 8, borderRadius: 8, background: "#ffffff" }} />
      <div
        style={{
          position: "absolute",
          left: 230,
          top: 308,
          width: 68,
          height: 68,
          borderRadius: "50%",
          background: accentColor,
          boxShadow: "0 14px 30px rgba(0,0,0,0.12)",
        }}
      />
    </div>
  );
};

export const NurseNarrationScene: React.FC<NurseNarrationSceneProps> = ({
  title,
  narration,
  accentColor,
  background,
  panel,
}) => {
  return (
    <AbsoluteFill style={{ background }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at top left, rgba(255,255,255,0.65), transparent 30%), radial-gradient(circle at bottom right, rgba(255,255,255,0.45), transparent 28%)",
        }}
      />
      <div style={{ position: "relative", zIndex: 1, width: "100%", height: "100%", display: "flex", alignItems: "center", padding: "52px 60px", gap: 28 }}>
        <div style={{ width: 360, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <NurseAvatar accentColor={accentColor} />
        </div>

        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 22 }}>
          <div style={{ color: "#16324f", fontSize: 24, fontWeight: 700, letterSpacing: 1.4, textTransform: "uppercase" }}>{title}</div>

          <div style={{ position: "relative", display: "flex", alignItems: "flex-start", gap: 18 }}>
            <div
              style={{
                position: "absolute",
                left: -18,
                top: 112,
                width: 0,
                height: 0,
                borderTop: "18px solid transparent",
                borderBottom: "18px solid transparent",
                borderRight: `28px solid ${accentColor}`,
                filter: "drop-shadow(0 10px 12px rgba(0,0,0,0.08))",
              }}
            />
            <div
              style={{
                flex: 1,
                background: "rgba(255,255,255,0.9)",
                border: `3px solid ${accentColor}`,
                borderRadius: 34,
                padding: "34px 38px",
                boxShadow: "0 18px 44px rgba(16, 52, 96, 0.14)",
                minHeight: 250,
              }}
            >
              <div style={{ color: "#243b53", fontSize: 24, lineHeight: 1.7, whiteSpace: "pre-wrap" }}>{narration}</div>
            </div>
          </div>

          {panel ? <div>{panel}</div> : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};