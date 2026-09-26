
import React from 'react'

const TONES = [
  'Professional',
  'Casual',
  'Formal',
  'Conversational',
  'Authoritative',
  'Friendly',
  'Persuasive',
  'Inspirational',
  'Technical',
  'Humorous',
]

const DETAIL_LEVELS = [
  'Very Concise',
  'Concise',
  'Moderate',
  'Comprehensive',
  'Very Detailed',
]

export default function ParametersPanel({ params, onChange }) {
  const set = (key) => (e) => onChange({ ...params, [key]: e.target.value })

  const inputClass =
    'w-full rounded-xl border border-white/60 bg-white/40 px-3.5 py-2.5 text-sm text-slate-800 shadow-inner outline-none backdrop-blur-md transition placeholder:text-slate-400 focus:border-slate-300 focus:bg-white/65 focus:ring-2 focus:ring-slate-200/60'

  const selectClass =
    'w-full rounded-xl border border-white/60 bg-white/40 px-3.5 py-2.5 text-sm text-slate-800 shadow-inner outline-none backdrop-blur-md transition focus:border-slate-300 focus:bg-white/65 focus:ring-2 focus:ring-slate-200/60'

  return (
    <section className="rounded-2xl border border-white/40 bg-white/55 shadow-[0_8px_32px_rgba(15,23,42,0.08)] backdrop-blur-xl">
      <div className="border-b border-white/40 px-4 py-4 sm:px-5">
        <h2 className="text-base font-semibold tracking-tight text-slate-900 sm:text-lg">
          Content Parameters
        </h2>

        <p className="mt-1 text-xs text-slate-500 sm:text-sm">
          Control how the output is written
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 p-4 sm:grid-cols-2 sm:p-5">
        <div>
          <label
            htmlFor="audience"
            className="mb-1.5 block text-xs font-medium text-slate-600"
          >
            Target Audience
          </label>

          <input
            id="audience"
            type="text"
            value={params.audience}
            onChange={set('audience')}
            placeholder="e.g. marketing managers"
            className={inputClass}
          />
        </div>

        <div>
          <label
            htmlFor="tone"
            className="mb-1.5 block text-xs font-medium text-slate-600"
          >
            Tone
          </label>

          <select
            id="tone"
            value={params.tone}
            onChange={set('tone')}
            className={selectClass}
          >
            {TONES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label
            htmlFor="language"
            className="mb-1.5 block text-xs font-medium text-slate-600"
          >
            Language
          </label>

          <input
            id="language"
            type="text"
            value={params.language}
            onChange={set('language')}
            className={inputClass}
          />
        </div>

        <div>
          <label
            htmlFor="detailLevel"
            className="mb-1.5 block text-xs font-medium text-slate-600"
          >
            Level of Detail
          </label>

          <select
            id="detailLevel"
            value={params.detail_level}
            onChange={set('detail_level')}
            className={selectClass}
          >
            {DETAIL_LEVELS.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label
            htmlFor="objective"
            className="mb-1.5 block text-xs font-medium text-slate-600"
          >
            Communication Objective
          </label>

          <input
            id="objective"
            type="text"
            value={params.objective}
            onChange={set('objective')}
            className={inputClass}
          />
        </div>

        <div>
          <label
            htmlFor="style"
            className="mb-1.5 block text-xs font-medium text-slate-600"
          >
            Content Style
          </label>

          <input
            id="style"
            type="text"
            value={params.style}
            onChange={set('style')}
            className={inputClass}
          />
        </div>

        <div className="sm:col-span-2">
          <div className="rounded-xl border border-white/50 bg-white/30 p-4 backdrop-blur-md">
            <div className="space-y-5">
              <div>
                <div className="mb-2 flex items-center justify-between">
                  <label
                    htmlFor="maxTokens"
                    className="text-xs font-medium text-slate-600"
                  >
                    Max Output Tokens
                  </label>

                  <strong className="text-xs text-slate-800">
                    {params.max_new_tokens}
                  </strong>
                </div>

                <input
                  id="maxTokens"
                  type="range"
                  min="256"
                  max="1024"
                  step="128"
                  value={params.max_new_tokens}
                  onChange={(e) =>
                    onChange({
                      ...params,
                      max_new_tokens: Number(e.target.value),
                    })
                  }
                  className="w-full cursor-pointer accent-slate-800"
                />
              </div>

              <div>
                <div className="mb-2 flex items-center justify-between">
                  <label
                    htmlFor="temperature"
                    className="text-xs font-medium text-slate-600"
                  >
                    Temperature
                  </label>

                  <strong className="text-xs text-slate-800">
                    {params.temperature.toFixed(2)}
                  </strong>
                </div>

                <input
                  id="temperature"
                  type="range"
                  min="0.1"
                  max="1.5"
                  step="0.05"
                  value={params.temperature}
                  onChange={(e) =>
                    onChange({
                      ...params,
                      temperature: Number(e.target.value),
                    })
                  }
                  className="w-full cursor-pointer accent-slate-800"
                />
              </div>

              <div>
                <div className="mb-2 flex items-center justify-between">
                  <label
                    htmlFor="topP"
                    className="text-xs font-medium text-slate-600"
                  >
                    Top-P
                  </label>

                  <strong className="text-xs text-slate-800">
                    {params.top_p.toFixed(2)}
                  </strong>
                </div>

                <input
                  id="topP"
                  type="range"
                  min="0.1"
                  max="1.0"
                  step="0.05"
                  value={params.top_p}
                  onChange={(e) =>
                    onChange({
                      ...params,
                      top_p: Number(e.target.value),
                    })
                  }
                  className="w-full cursor-pointer accent-slate-800"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

