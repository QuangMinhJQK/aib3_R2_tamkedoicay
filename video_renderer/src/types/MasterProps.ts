export interface HealthMetric {
  label: string;
  value: string | number;
  trend: 'up' | 'down' | 'stable';
  unit?: string;
}

export interface DoctorAdvice {
  text: string;
  audioDurationInFrames: number;
}

export interface SectionNarration {
  section: 'report_status' | 'health_metrics' | 'progress' | 'advice';
  text: string;
  audioDurationInFrames: number;
}

export interface MasterProps {
  patientName: string;
  overallStatus: string;
  metrics: HealthMetric[];
  advices: DoctorAdvice[];
  sectionNarrations?: SectionNarration[];
  sectionDurationsInFrames?: {
    report_status: number;
    health_metrics: number;
    progress: number;
    advice: number;
  };
  totalDurationInFrames: number;
}
