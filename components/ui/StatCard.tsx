import { ReactNode } from "react";
import { Sparkline } from "@/components/charts/Sparkline";

type Tone = "good" | "warn" | "bad" | "neutral";

type StatCardProps = {
  label: string;
  value: string;
  sub?: string;
  tone?: Tone;
  icon?: ReactNode;
  series?: number[];
};

export function StatCard({ label, value, sub, tone = "neutral", icon, series = [] }: StatCardProps) {
  const toneClass = tone === "neutral" ? "" : tone;
  return (
    <article className="card clean-card stat-card">
      <div className="stat-head">
        <h3>{label}</h3>
        {icon ? <span className="stat-icon">{icon}</span> : null}
      </div>
      <div className={`metric ${toneClass}`}>{value}</div>
      {sub ? <p className="metric-sub">{sub}</p> : null}
      {series.length ? (
        <div className="sparkline-wrap">
          <Sparkline values={series} tone={tone} />
        </div>
      ) : null}
    </article>
  );
}
