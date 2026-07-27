import { useState } from 'react'
import { predictUrl } from '../api/client.js'

export default function UrlChecker() {
  const [url, setUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    const trimmed = url.trim()
    if (!trimmed) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const data = await predictUrl(trimmed)
      setResult(data)
    } catch (err) {
      setError(
        err?.response?.data?.detail
          ? JSON.stringify(err.response.data.detail)
          : err.message || 'Request failed. Is the backend running?'
      )
    } finally {
      setLoading(false)
    }
  }

  const pct = result ? Math.round(result.confidence * 100) : 0

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-slate-800">Check a URL</h1>
        <p className="mt-2 text-slate-500">
          Enter any URL to check whether it looks like a phishing site.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com/login"
          className="flex-1 rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-800 placeholder-slate-400 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
        />
        <button
          type="submit"
          disabled={loading || !url.trim()}
          className="rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white shadow-sm hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Checking…' : 'Check'}
        </button>
      </form>

      {error && (
        <div className="mt-6 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {error}
        </div>
      )}

      {result && (
        <div
          className={`mt-8 rounded-2xl border p-6 shadow-sm ${
            result.is_phishing
              ? 'border-rose-200 bg-rose-50'
              : 'border-emerald-200 bg-emerald-50'
          }`}
        >
          <div className="flex items-center gap-3">
            <span
              className={`flex h-11 w-11 items-center justify-center rounded-full text-white text-xl ${
                result.is_phishing ? 'bg-rose-500' : 'bg-emerald-500'
              }`}
            >
              {result.is_phishing ? '⚠' : '✓'}
            </span>
            <div>
              <p
                className={`text-lg font-bold ${
                  result.is_phishing ? 'text-rose-700' : 'text-emerald-700'
                }`}
              >
                {result.is_phishing ? 'Phishing detected!' : 'Looks safe'}
              </p>
              <p className="text-sm text-slate-500 break-all">{result.url}</p>
            </div>
          </div>

          <div className="mt-5">
            <div className="flex justify-between text-sm font-medium text-slate-600">
              <span>Confidence</span>
              <span className="tabular-nums">{pct}%</span>
            </div>
            <div className="mt-1 h-2.5 w-full overflow-hidden rounded-full bg-white/70">
              <div
                className={`h-full rounded-full ${
                  result.is_phishing ? 'bg-rose-500' : 'bg-emerald-500'
                }`}
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
