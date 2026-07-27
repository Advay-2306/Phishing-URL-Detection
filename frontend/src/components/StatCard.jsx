export default function StatCard({ label, value, sub, accent = 'blue' }) {
  const accents = {
    blue: 'from-blue-500 to-blue-600',
    red: 'from-rose-500 to-rose-600',
    green: 'from-emerald-500 to-emerald-600',
    amber: 'from-amber-500 to-amber-600',
  }
  return (
    <div className="rounded-2xl bg-white border border-slate-200 shadow-sm p-5">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">{label}</p>
        <span
          className={`inline-block w-2.5 h-2.5 rounded-full bg-gradient-to-br ${
            accents[accent] || accents.blue
          }`}
        />
      </div>
      <p className="mt-2 text-3xl font-bold text-slate-800 tabular-nums">{value}</p>
      {sub && <p className="mt-1 text-xs text-slate-400">{sub}</p>}
    </div>
  )
}
