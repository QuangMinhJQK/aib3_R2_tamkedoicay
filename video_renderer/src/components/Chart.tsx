import { AbsoluteFill } from "remotion";

export const Chart: React.FC = () => {
  return (
    <div style={{
      width: '100%',
      minHeight: '300px',
      background: 'linear-gradient(180deg, rgba(255,255,255,0.9) 0%, rgba(236,247,255,0.95) 100%)',
      borderRadius: '28px',
      border: '2px solid rgba(47, 128, 237, 0.18)',
      boxShadow: '0 18px 42px rgba(16, 52, 96, 0.12)',
      color: '#17324d',
      fontFamily: 'sans-serif',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      flexDirection: 'column',
      gap: '14px'
    }}>
      <h1 style={{ fontSize: '52px', color: '#eb5757', margin: 0 }}>Clinical Progress</h1>
      <div style={{ width: '70%', height: '10px', borderRadius: '999px', background: 'linear-gradient(90deg, #7fd0ff 0%, #7ee8a6 50%, #ffd166 100%)' }} />
      {/* TODO: Add SVG or Canvas chart here */}
    </div>
  );
};
