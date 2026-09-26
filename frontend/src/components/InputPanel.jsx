
import React, { useState } from 'react'

export default function InputPanel({ value, onChange }) {
  const [fileName, setFileName] = useState(null)
  const [error, setError] = useState(null)

  async function handleFile(event) {
    const file = event.target.files?.[0]
    if (!file) return
    setError(null)

    const ext = file.name.split('.').pop().toLowerCase()

    if (ext === 'txt' || ext === 'md') {
      const text = await file.text()
      onChange(text)
      setFileName(file.name)
      return
    }

    if (ext === 'pdf' || ext === 'docx') {
      setError(
        'PDF and DOCX extraction requires the backend. Paste the text directly instead.',
      )
      event.target.value = ''
      return
    }

    setError(`Unsupported file type: .${ext}`)
    event.target.value = ''
  }

  return (
    <section className="rounded-2xl border border-white/40 bg-white/55 shadow-[0_8px_32px_rgba(15,23,42,0.08)] backdrop-blur-xl">
      <div className="flex flex-col gap-1 border-b border-white/40 px-4 py-4 sm:px-5">
        <h2 className="text-base font-semibold tracking-tight text-slate-900 sm:text-lg">
          Source Content
        </h2>

        <p className="text-xs text-slate-500 sm:text-sm">
          The material you want to transform
        </p>
      </div>

      <div className="p-4 sm:p-5">
        <textarea
          className="min-h-[230px] w-full resize-y rounded-xl border border-white/60 bg-white/45 p-4 text-sm leading-6 text-slate-800 shadow-inner outline-none backdrop-blur-md transition placeholder:text-slate-400 focus:border-slate-300 focus:bg-white/65 focus:ring-2 focus:ring-slate-200/60 sm:min-h-[270px]"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Paste text or upload document(.txt, .md, .pdf, .docx)"
          rows={10}
        />

        <div className="mt-3 flex flex-col gap-2 sm:flex-row sm:items-center">
          <label className="inline-flex w-full cursor-pointer items-center justify-center rounded-xl border border-white/60 bg-white/50 px-4 py-2.5 text-sm font-medium text-slate-700 shadow-sm backdrop-blur-md transition hover:bg-white/70 sm:w-auto">
            Upload File 

            <input
              type="file"
              accept=".txt,.md ,.pdf,.docx"
              onChange={handleFile}
              className="hidden"
            />
          </label>

          {fileName && (
            <span className="truncate rounded-lg border border-white/40 bg-white/35 px-3 py-2 text-xs text-slate-600 backdrop-blur-md">
              {fileName}
            </span>
          )}
        </div>

        {error && (
          <p className="mt-3 rounded-xl border border-red-200/60 bg-red-50/60 px-3 py-2.5 text-xs leading-5 text-red-700 backdrop-blur-md">
            {error}
          </p>
        )}

        <div className="mt-3 text-right text-xs text-slate-400">
          {value.length.toLocaleString()} characters
        </div>
      </div>
    </section>
  )
}

