'use client'

import { useState, type FormEvent } from 'react'

type Citation = { id: number; source: string; page: number; score: number | null }
type AskResult = { answer: string; citations: Citation[] }
type UploadStatus = 'idle' | 'uploading' | 'done' | 'error'

export default function Home() {
  const [file, setFile] = useState<File>()
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>('idle')
  const [uploadedName, setUploadedName] = useState<string>()

  const [query, setQuery] = useState('')
  const [result, setResult] = useState<AskResult>()
  const [loading, setLoading] = useState(false)
  const [askError, setAskError] = useState<string>()

  const onUpload = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!file) return
    setUploadStatus('uploading')

    try {
      const data = new FormData()
      data.set('file', file)

      const res = await fetch('/api/uploads', { method: 'POST', body: data })
      if (!res.ok) throw new Error(await res.text())

      setUploadedName(file.name)
      setUploadStatus('done')
    } catch (err) {
      console.error(err)
      setUploadStatus('error')
    }
  }

  const onAsk = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    setAskError(undefined)

    try {
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      })
      if (!res.ok) throw new Error(await res.text())
      setResult(await res.json())
    } catch (err) {
      console.error(err)
      setAskError('Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen w-full bg-rose-50 px-4 py-12 text-stone-800">
      <div className="mx-auto w-full max-w-2xl space-y-8">
        {/* Header */}
        <header className="space-y-1 text-center">
          <h1 className="text-3xl font-semibold tracking-tight">
            Agentic <span className="text-rose-400">Research</span> Assistant
          </h1>
          <p className="text-sm text-stone-500">
            Upload a document, then ask questions about it.
          </p>
        </header>

        {/* 1 · Upload */}
        <section className="rounded-2xl border border-rose-100 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xs font-semibold uppercase tracking-wide text-stone-400">
            1 · Upload a document
          </h2>
          <form onSubmit={onUpload} className="flex flex-wrap items-center gap-3">
            <input
              type="file"
              name="file"
              onChange={(e) => {
                setFile(e.target.files?.[0])
                setUploadStatus('idle')
              }}
              className="flex-1 text-sm text-stone-600 file:mr-3 file:cursor-pointer file:rounded-full file:border-0 file:bg-rose-100 file:px-4 file:py-2 file:text-sm file:font-medium file:text-rose-600 hover:file:bg-rose-200"
            />
            <button
              type="submit"
              disabled={!file || uploadStatus === 'uploading'}
              className="rounded-full bg-rose-400 px-5 py-2 text-sm font-medium text-white transition hover:bg-rose-500 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {uploadStatus === 'uploading' ? 'Uploading…' : 'Upload'}
            </button>
          </form>

          {uploadStatus === 'done' && (
            <p className="mt-3 text-sm text-emerald-600">
              ✓ Added “{uploadedName}”
            </p>
          )}
          {uploadStatus === 'error' && (
            <p className="mt-3 text-sm text-rose-500">
              Upload failed. Please try again.
            </p>
          )}
        </section>

        {/* 2 · Ask */}
        <section className="rounded-2xl border border-rose-100 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xs font-semibold uppercase tracking-wide text-stone-400">
            2 · Ask a question
          </h2>
          <form onSubmit={onAsk} className="flex flex-wrap items-center gap-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask about your documents…"
              className="flex-1 rounded-full border border-stone-200 bg-rose-50/40 px-5 py-2.5 text-sm text-stone-800 placeholder:text-stone-400 focus:border-rose-300 focus:outline-none focus:ring-2 focus:ring-rose-200"
            />
            <button
              type="submit"
              disabled={!query.trim() || loading}
              className="rounded-full bg-rose-400 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-rose-500 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading ? 'Thinking…' : 'Ask'}
            </button>
          </form>
        </section>

        {/* Answer */}
        {(loading || askError || result) && (
          <section className="rounded-2xl border border-rose-100 bg-white p-6 shadow-sm">
            <h2 className="mb-4 text-xs font-semibold uppercase tracking-wide text-stone-400">
              Answer
            </h2>

            {loading && (
              <p className="animate-pulse text-sm text-stone-400">Thinking…</p>
            )}

            {askError && !loading && (
              <p className="text-sm text-rose-500">{askError}</p>
            )}

            {result && !loading && (
              <div className="space-y-5">
                <p className="whitespace-pre-wrap leading-relaxed text-stone-700">
                  {result.answer}
                </p>

                {result.citations.length > 0 && (
                  <div className="space-y-2 border-t border-rose-100 pt-4">
                    <p className="text-xs font-semibold uppercase tracking-wide text-stone-400">
                      Sources
                    </p>
                    <ul className="flex flex-wrap gap-2">
                      {result.citations.map((c) => (
                        <li
                          key={c.id}
                          className="rounded-full bg-rose-100 px-3 py-1 text-xs text-rose-700"
                        >
                          [{c.id}] {c.source} · p.{c.page}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </section>
        )}
      </div>
    </main>
  )
}
