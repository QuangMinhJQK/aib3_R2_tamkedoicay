import { DoctorAdvice as DoctorAdviceType } from "../types/MasterProps";

export const DoctorAdvice: React.FC<{ advices: DoctorAdviceType[] }> = ({ advices }) => {
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
      maxWidth: '760px'
    }}>
      <h1 style={{ fontSize: '40px', color: '#2f80ed', margin: 0 }}>Doctor's Advice</h1>
      <div style={{ maxWidth: '800px', textAlign: 'left' }}>
        {advices.map((a, i) => (
          <p key={i} style={{
            fontSize: '28px',
            lineHeight: '1.5',
            margin: '16px 0',
            background: 'linear-gradient(180deg, #ffffff 0%, #ecf7ff 100%)',
            padding: '22px',
            borderRadius: '20px',
            boxShadow: '0 10px 20px rgba(0,0,0,0.08)',
            border: '1px solid rgba(47, 128, 237, 0.14)'
          }}>
            {a.text}
          </p>
        ))}
      </div>
    </div>
  );
};
