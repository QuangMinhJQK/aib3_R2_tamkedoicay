import { AbsoluteFill, Sequence } from "remotion";
import { MasterProps } from "./types/MasterProps";
import { HealthCard } from "./components/HealthCard";
import { DoctorAdvice } from "./components/DoctorAdvice";
import { Chart } from "./components/Chart";

export const MainComposition: React.FC<MasterProps> = ({ patientName, overallStatus, metrics, advices, totalDurationInFrames }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0f3460' }}>
      <Sequence from={0} durationInFrames={90}>
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', color: 'white', fontFamily: 'sans-serif' }}>
          <h1 style={{ fontSize: '60px' }}>Health Report: {patientName}</h1>
          <h2 style={{ fontSize: '40px', color: '#00d2ff' }}>Status: {overallStatus}</h2>
        </AbsoluteFill>
      </Sequence>
      
      <Sequence from={90} durationInFrames={120}>
        <HealthCard metrics={metrics} />
      </Sequence>
      
      <Sequence from={210} durationInFrames={120}>
        <Chart />
      </Sequence>
      
      <Sequence from={330} durationInFrames={Math.max(120, totalDurationInFrames - 330)}>
        <DoctorAdvice advices={advices} />
      </Sequence>
    </AbsoluteFill>
  );
};
