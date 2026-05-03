import { HealthMetric } from "../types/MasterProps";

export const HealthCard: React.FC<{ metrics: HealthMetric[] }> = ({ metrics }) => {
  return (
    <div style={{
      width: '100%',
      color: '#17324d',
      fontFamily: 'sans-serif',
      padding: '28px',
      display: 'flex',
      flexDirection: 'column',
      gap: '18px',
      background: 'rgba(255,255,255,0.82)',
      borderRadius: '28px',
      border: '2px solid rgba(63, 168, 255, 0.28)',
      boxShadow: '0 18px 42px rgba(16, 52, 96, 0.12)',
    }}>
      <h1 style={{ fontSize: '40px', margin: 0, color: '#2f80ed' }}>Health Metrics</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px' }}>
        {metrics.map((m, i) => (
          <div key={i} style={{
            background: 'linear-gradient(180deg, #ffffff 0%, #ecf7ff 100%)',
            padding: '18px',
            borderRadius: '18px',
            minWidth: '220px',
            border: '1px solid rgba(47, 128, 237, 0.18)'
          }}>
            <h2 style={{ fontSize: '24px', margin: 0, color: '#eb5757' }}>{m.label}</h2>
            <p style={{ fontSize: '34px', margin: '8px 0', fontWeight: 'bold', color: '#17324d' }}>{m.value} <span style={{ fontSize: '18px', color: '#6b7c93' }}>{m.unit}</span></p>
            <p style={{ fontSize: '20px', margin: 0, color: '#355c7d' }}>Trend: {m.trend === 'up' ? '↑ Up' : m.trend === 'down' ? '↓ Down' : '→ Stable'}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
