type SparklineProps = {
  values: number[];
  tone?: "good" | "warn" | "bad" | "neutral";
};

export function Sparkline({ values, tone = "neutral" }: SparklineProps) {
  const safe = values.length > 1 ? values : [0, 0];
  const min = Math.min(...safe);
  const max = Math.max(...safe);
  const range = max - min || 1;

  const points = safe
    .map((v, i) => {
      const x = (i / (safe.length - 1)) * 100;
      const y = 100 - ((v - min) / range) * 100;
      return `${x},${y}`;
    })
    .join(" ");

  const area = `0,100 ${points} 100,100`;

  return (
    <svg viewBox="0 0 100 100" preserveAspectRatio="none" className={`sparkline ${tone}`}>
      <polygon className="sparkline-area" points={area} />
      <polyline className="sparkline-line" fill="none" points={points} />
    </svg>
  );
}
