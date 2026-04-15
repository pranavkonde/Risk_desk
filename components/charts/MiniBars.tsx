type Row = { label: string; value: number; note?: string };

type MiniBarsProps = {
  title: string;
  rows: Row[];
  positiveIsGood?: boolean;
};

export function MiniBars({ title, rows, positiveIsGood = true }: MiniBarsProps) {
  const max = Math.max(...rows.map((r) => Math.abs(r.value)), 1);

  return (
    <div className="card clean-card chart-card">
      <h3 className="chart-title">{title}</h3>
      <div className="bars">
        {rows.map((r) => {
          const width = (Math.abs(r.value) / max) * 100;
          const isPositive = r.value >= 0;
          const tone = isPositive === positiveIsGood ? "good" : "bad";
          return (
            <div className="bar-row" key={r.label}>
              <div className="bar-label">
                <span>{r.label}</span>
                <span className={tone}>{r.value.toFixed(4)}</span>
              </div>
              <div className="bar-track">
                <div className={`bar-fill ${tone}`} style={{ width: `${Math.max(width, 4)}%` }} />
              </div>
              {r.note ? <p className="bar-note">{r.note}</p> : null}
            </div>
          );
        })}
      </div>
    </div>
  );
}
