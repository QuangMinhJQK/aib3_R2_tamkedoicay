import { AbsoluteFill } from "remotion";
import { DoctorAdvice as DoctorAdviceType } from "../types/MasterProps";

export const DoctorAdvice: React.FC<{ advices: DoctorAdviceType[] }> = ({ advices }) => {
  return (
    <AbsoluteFill style={{
      backgroundColor: '#1a1a2e',
      color: 'white',
      fontFamily: 'sans-serif',
      padding: '60px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center'
    }}>
      <h1 style={{ fontSize: '50px', color: '#00d2ff', marginBottom: '40px' }}>Doctor's Advice</h1>
      <div style={{ maxWidth: '800px', textAlign: 'center' }}>
        {advices.map((a, i) => (
          <p key={i} style={{
            fontSize: '36px',
            lineHeight: '1.5',
            margin: '20px 0',
            backgroundColor: '#16213e',
            padding: '30px',
            borderRadius: '20px',
            boxShadow: '0 10px 20px rgba(0,0,0,0.3)'
          }}>
            {a.text}
          </p>
        ))}
      </div>
    </AbsoluteFill>
  );
};
