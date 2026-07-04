export function MissionProgressBar({ completed, total }: { completed: number; total: number }) {
  const value = total === 0 ? 0 : Math.round((completed / total) * 100);
  return (
    <div>
      <div className="mb-2 flex justify-between text-xs text-steel">
        <span>Mission progress</span>
        <span>{value}%</span>
      </div>
      <div className="h-2 rounded-sm bg-line">
        <div className="h-2 rounded-sm bg-silver" style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}
