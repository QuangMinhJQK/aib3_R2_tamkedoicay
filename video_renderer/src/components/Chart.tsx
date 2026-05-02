import { AbsoluteFill } from "remotion";

export const Chart: React.FC = () => {
  return (
    <AbsoluteFill style={{
      backgroundColor: '#1a1a2e',
      color: 'white',
      fontFamily: 'sans-serif',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center'
    }}>
      <h1 style={{ fontSize: '80px', color: '#e94560' }}>Clinical Progress</h1>
      {/* TODO: Add SVG or Canvas chart here */}
    </AbsoluteFill>
  );
};
