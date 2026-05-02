import { AbsoluteFill } from "remotion";
import { HealthMetric } from "../types/MasterProps";

export const HealthCard: React.FC<{ metrics: HealthMetric[] }> = ({ metrics }) => {
  return (
    <AbsoluteFill style={{
      backgroundColor: '#1a1a2e',
      color: 'white',
      fontFamily: 'sans-serif',
      padding: '40px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
    }}>
      <h1 style={{ fontSize: '60px', marginBottom: '40px', color: '#00d2ff' }}>Health Metrics</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px' }}>
        {metrics.map((m, i) => (
          <div key={i} style={{
            backgroundColor: '#16213e',
            padding: '20px',
            borderRadius: '16px',
            minWidth: '250px',
            border: '1px solid #0f3460'
          }}>
            <h2 style={{ fontSize: '30px', margin: 0, color: '#e94560' }}>{m.label}</h2>
            <p style={{ fontSize: '40px', margin: '10px 0', fontWeight: 'bold' }}>{m.value} <span style={{ fontSize: '20px', color: '#888' }}>{m.unit}</span></p>
            <p style={{ fontSize: '24px', margin: 0 }}>Trend: {m.trend === 'up' ? '↑ Up' : m.trend === 'down' ? '↓ Down' : '→ Stable'}</p>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
