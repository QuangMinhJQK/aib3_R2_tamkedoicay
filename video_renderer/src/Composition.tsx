import { AbsoluteFill, Sequence } from "remotion";
import { MasterProps } from "./types/MasterProps";
import { HealthCard } from "./components/HealthCard";
import { Chart } from "./components/Chart";
import { NurseNarrationScene } from "./components/NurseNarrationScene";

const getSectionNarration = (sectionNarrations: MasterProps["sectionNarrations"], section: string, fallback: string) => {
  return sectionNarrations?.find((item) => item.section === section)?.text || fallback;
};

export const MainComposition: React.FC<MasterProps> = ({ patientName, overallStatus, metrics, advices, sectionNarrations, sectionDurationsInFrames, totalDurationInFrames }) => {
  const sectionDurations = sectionDurationsInFrames;

  const reportFrames = Math.max(1, sectionDurations?.report_status ?? 90);
  const metricsFrames = Math.max(1, sectionDurations?.health_metrics ?? 120);
  const progressFrames = Math.max(1, sectionDurations?.progress ?? 120);
  const adviceFrames = Math.max(1, sectionDurations?.advice ?? Math.max(120, totalDurationInFrames - 330));

  const reportStart = 0;
  const metricsStart = reportStart + reportFrames;
  const progressStart = metricsStart + metricsFrames;
  const adviceStart = progressStart + progressFrames;

  const reportNarration = getSectionNarration(
    sectionNarrations,
    "report_status",
    `Here is the health report for ${patientName}. The overall status is ${overallStatus}.`
  );
  const metricsNarration = getSectionNarration(
    sectionNarrations,
    "health_metrics",
    "These are the key health metrics shown on the dashboard."
  );
  const progressNarration = getSectionNarration(
    sectionNarrations,
    "progress",
    "This section highlights recent clinical progress and trends."
  );
  const adviceNarration = getSectionNarration(
    sectionNarrations,
    "advice",
    "Please follow the recommendations shown here and keep your routine consistent."
  );

  return (
    <AbsoluteFill style={{ background: 'linear-gradient(135deg, #f4fbff 0%, #dff4ff 45%, #eafaf1 100%)' }}>
      <Sequence from={reportStart} durationInFrames={reportFrames}>
        <NurseNarrationScene
          title="Report Status"
          narration={reportNarration}
          accentColor="#3fa8ff"
          background="linear-gradient(135deg, #f4fbff 0%, #dff4ff 100%)"
          panel={
            <div style={{ marginTop: 10, maxWidth: 840 }}>
              <div style={{ background: 'rgba(255,255,255,0.72)', borderRadius: 24, padding: 28, boxShadow: '0 18px 42px rgba(16, 52, 96, 0.10)' }}>
                <h1 style={{ fontSize: 42, margin: 0, color: '#17324d' }}>Health Report: {patientName}</h1>
                <h2 style={{ fontSize: 28, marginTop: 12, color: '#2f80ed' }}>Status: {overallStatus}</h2>
              </div>
            </div>
          }
        />
      </Sequence>
      
      <Sequence from={metricsStart} durationInFrames={metricsFrames}>
        <NurseNarrationScene
          title="Health Metrics"
          narration={metricsNarration}
          accentColor="#7ee8a6"
          background="linear-gradient(135deg, #f3fff8 0%, #e4fff1 100%)"
          panel={<HealthCard metrics={metrics} />}
        />
      </Sequence>
      
      <Sequence from={progressStart} durationInFrames={progressFrames}>
        <NurseNarrationScene
          title="Clinical Progress"
          narration={progressNarration}
          accentColor="#ffd166"
          background="linear-gradient(135deg, #fffdf4 0%, #fff3d9 100%)"
          panel={<Chart />}
        />
      </Sequence>
      
      <Sequence from={adviceStart} durationInFrames={adviceFrames}>
        <NurseNarrationScene
          title="Doctor's Advice"
          narration={adviceNarration}
          accentColor="#ff8fb1"
          background="linear-gradient(135deg, #fff7fb 0%, #ffe7f0 100%)"
        />
      </Sequence>
    </AbsoluteFill>
  );
};
