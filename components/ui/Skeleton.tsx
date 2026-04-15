type SkeletonProps = {
  lines?: number;
};

export function SkeletonBlock({ lines = 4 }: SkeletonProps) {
  return (
    <div className="skeleton-wrap" aria-busy="true" aria-live="polite">
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} className="skeleton-line" />
      ))}
    </div>
  );
}
