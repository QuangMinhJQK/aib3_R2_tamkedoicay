import "./index.css";
import { Composition } from "remotion";
import { MainComposition } from "./Composition";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="CareLoopVideo"
        component={MainComposition as React.FC<any>}
        durationInFrames={900}
        fps={30}
        width={1280}
        height={720}
        defaultProps={{
          patientName: "",
          overallStatus: "",
          metrics: [],
          advices: [],
          sectionNarrations: [],
          sectionDurationsInFrames: {
            report_status: 180,
            health_metrics: 240,
            progress: 240,
            advice: 240,
          },
          totalDurationInFrames: 900,
        }}
      />
    </>
  );
};
