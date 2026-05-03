import { ClinicalMetricSeries } from "../types/MasterProps";

type ChartProps = {
  series?: ClinicalMetricSeries[];
};

const MAX_VISIBLE_SERIES = 4;
const MAX_VISIBLE_POINTS = 8;

const formatValue = (value: number) => {
  return Number.isInteger(value) ? value.toString() : value.toFixed(1);
};

const SeriesCard: React.FC<{ item: ClinicalMetricSeries }> = ({ item }) => {
  const points = item.points.slice(-MAX_VISIBLE_POINTS);
  if (points.length === 0) {
    return (
      <div
        style={{
          background: "linear-gradient(180deg, #ffffff 0%, #f4f9ff 100%)",
          borderRadius: 24,
          border: "1px solid rgba(47, 128, 237, 0.16)",
          boxShadow: "0 16px 34px rgba(16, 52, 96, 0.08)",
          padding: 18,
          minHeight: 180,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#607086",
          fontSize: 16,
        }}
      >
        No points available for {item.name}.
      </div>
    );
  }

  const width = 520;
  const height = 180;
  const paddingX = 28;
  const paddingY = 24;
  const values = points.map((point) => point.value);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = Math.max(1, max - min);
  const stepX = points.length > 1 ? (width - paddingX * 2) / (points.length - 1) : 0;

  const getY = (value: number) => {
    const normalized = (value - min) / range;
    return height - paddingY - normalized * (height - paddingY * 2);
  };

  const polyline = points
    .map((point, index) => `${paddingX + index * stepX},${getY(point.value)}`)
    .join(" ");

  const isTruncated = item.totalPoints > MAX_VISIBLE_POINTS;

  return (
    <div
      style={{
        background: "linear-gradient(180deg, #ffffff 0%, #f4f9ff 100%)",
        borderRadius: 24,
        border: "1px solid rgba(47, 128, 237, 0.16)",
        boxShadow: "0 16px 34px rgba(16, 52, 96, 0.08)",
        padding: 18,
        minHeight: 260,
        overflow: "hidden",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12, marginBottom: 12 }}>
        <div>
          <div style={{ fontSize: 22, fontWeight: 700, color: "#17324d", lineHeight: 1.2 }}>{item.name}</div>
          <div style={{ fontSize: 15, color: "#607086", marginTop: 4 }}>
            {item.points.length} điểm gần nhất{item.unit ? ` • ${item.unit}` : ""}
          </div>
        </div>
        {isTruncated ? (
          <div style={{ fontSize: 12, color: "#2f80ed", background: "rgba(47, 128, 237, 0.1)", padding: "6px 10px", borderRadius: 999 }}>
            +{item.totalPoints - points.length} more
          </div>
        ) : null}
      </div>

      <svg viewBox={`0 0 ${width} ${height}`} width="100%" height="180" preserveAspectRatio="none" style={{ display: "block" }}>
        <defs>
          <linearGradient id={`series-fill-${item.name.replace(/\s+/g, "-")}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#7fd0ff" stopOpacity="0.42" />
            <stop offset="100%" stopColor="#7fd0ff" stopOpacity="0.03" />
          </linearGradient>
        </defs>
        <line x1={paddingX} y1={height - paddingY} x2={width - paddingX} y2={height - paddingY} stroke="#dbe8f5" strokeWidth="2" />
        <polyline
          fill="none"
          stroke="#2f80ed"
          strokeWidth="5"
          strokeLinecap="round"
          strokeLinejoin="round"
          points={polyline}
        />
        <polygon
          points={`${paddingX},${height - paddingY} ${polyline} ${width - paddingX},${height - paddingY}`}
          fill={`url(#series-fill-${item.name.replace(/\s+/g, "-")})`}
          opacity="0.8"
        />
        {points.map((point, index) => (
          <g key={`${item.name}-${point.date}-${index}`}>
            <circle cx={paddingX + index * stepX} cy={getY(point.value)} r="7" fill="#ffffff" stroke="#2f80ed" strokeWidth="4" />
            <text
              x={paddingX + index * stepX}
              y={height - 2}
              textAnchor="middle"
              fontSize="14"
              fill="#607086"
            >
              {point.date}
            </text>
          </g>
        ))}
      </svg>

      <div style={{ display: "flex", flexWrap: "wrap", gap: 10, marginTop: 12 }}>
        {points.map((point, index) => (
          <div
            key={`${item.name}-summary-${point.date}-${index}`}
            style={{
              minWidth: 92,
              flex: "1 1 92px",
              background: "rgba(47, 128, 237, 0.06)",
              borderRadius: 14,
              padding: "10px 12px",
            }}
          >
            <div style={{ fontSize: 12, color: "#607086" }}>{point.date}</div>
            <div style={{ fontSize: 22, fontWeight: 700, color: "#17324d", marginTop: 4 }}>{formatValue(point.value)}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export const Chart: React.FC<ChartProps> = ({ series = [] }) => {
  const visibleSeries = series.slice(0, MAX_VISIBLE_SERIES);
  const overflowCount = Math.max(0, series.length - visibleSeries.length);

  return (
    <div
      style={{
        width: "100%",
        color: "#17324d",
        fontFamily: "sans-serif",
        padding: 24,
        display: "flex",
        flexDirection: "column",
        gap: 16,
        background: "rgba(255,255,255,0.84)",
        borderRadius: 28,
        border: "2px solid rgba(47, 128, 237, 0.18)",
        boxShadow: "0 18px 42px rgba(16, 52, 96, 0.12)",
        overflow: "hidden",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", gap: 16, flexWrap: "wrap" }}>
        <div>
          <div style={{ fontSize: 40, fontWeight: 800, color: "#2f80ed", lineHeight: 1.1 }}>Clinical Progress</div>
        </div>
        {overflowCount > 0 ? (
          <div style={{ fontSize: 13, color: "#2f80ed", background: "rgba(47, 128, 237, 0.1)", padding: "8px 12px", borderRadius: 999 }}>
            +{overflowCount} more series omitted
          </div>
        ) : null}
      </div>

      {visibleSeries.length > 0 ? (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: 16,
            alignItems: "stretch",
          }}
        >
          {visibleSeries.map((item) => (
            <SeriesCard key={item.name} item={item} />
          ))}
        </div>
      ) : (
        <div
          style={{
            minHeight: 260,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            borderRadius: 24,
            background: "linear-gradient(180deg, #ffffff 0%, #eef6ff 100%)",
            border: "1px dashed rgba(47, 128, 237, 0.24)",
            color: "#607086",
            fontSize: 18,
          }}
        >
          No clinical history available yet.
        </div>
      )}
    </div>
  );
};
