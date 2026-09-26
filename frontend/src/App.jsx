
import React, { useState, useEffect, useMemo } from 'react'
import InputPanel from './components/InputPanel'
import OutputTypeSelector from './components/OutputTypeSelector'
import ParametersPanel from './components/ParametersPanel'
import OutputPanel from './components/OutputPanel'
import { fetchModelInfo, generateContent } from './services/api'

const DEFAULT_PARAMS = {
  audience: 'general professional audience',
  tone: 'Professional',
  language: 'English',
  detail_level: 'Moderate',
  objective: 'inform and engage',
  style: 'professional',
  max_new_tokens: 1024,
  temperature: 0.7,
  top_p: 0.9,
}

export default function App() {
  const [sourceContent, setSourceContent] = useState('')
  const [selectedOutputs, setSelectedOutputs] = useState([])
  const [params, setParams] = useState(DEFAULT_PARAMS)
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [currentType, setCurrentType] = useState(null)
  const [modelInfo, setModelInfo] = useState(null)
  const [apiError, setApiError] = useState(null)

  // Profile dropdown state
  const [isProfileOpen, setIsProfileOpen] = useState(false)

  useEffect(() => {
    fetchModelInfo()
      .then(setModelInfo)
      .catch(() =>
        setModelInfo({
          name: 'TinyLlama-1.1B-Chat-v1.0',
          backend: 'checking...',
        }),
      )
  }, [])

  function toggleOutput(name) {
    setSelectedOutputs((prev) =>
      prev.includes(name)
        ? prev.filter((n) => n !== name)
        : [...prev, name],
    )
  }

  function canGenerate() {
    return (
      sourceContent.trim().length > 0 &&
      selectedOutputs.length > 0 &&
      !loading
    )
  }

  async function handleGenerate() {
    if (!canGenerate()) return

    setLoading(true)
    setResults([])
    setApiError(null)

    try {
      for (const outputType of selectedOutputs) {
        setCurrentType(outputType)

        const result = await generateContent({
          output_type: outputType,
          source_content: sourceContent,
          audience: params.audience,
          tone: params.tone,
          language: params.language,
          detail_level: params.detail_level,
          objective: params.objective,
          style: params.style,
          max_new_tokens: params.max_new_tokens,
          temperature: params.temperature,
          top_p: params.top_p,
        })

        setResults((prev) => [...prev, result])
      }
    } catch (err) {
      setApiError(err.message)
    } finally {
      setLoading(false)
      setCurrentType(null)
    }
  }

  const backup = useMemo(
    () =>
      modelInfo && modelInfo.backend
        ? modelInfo.backend.replace('_', ' ')
        : 'loading model...',
    [modelInfo],
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-500 via-slate-50 to-white text-slate-900">
    <header className="relative z-[100] border-b border-white/50 bg-white/45 backdrop-blur-xl">
        <div className="mx-auto flex min-h-[72px] w-full max-w-7xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
          <img
            src="/saar-ai.svg"
            alt="सार AI"
            className="h-15 w-auto"
          />

          {/* Profile Dropdown */}
         <div className="relative z-[110]">
            <button
              type="button"
              onClick={() => setIsProfileOpen((prev) => !prev)}
              className="rounded-full border border-white/60 bg-white/40 p-1 shadow-sm backdrop-blur-md transition hover:bg-white/60"
            >
              <img
                src="/profile.png"
                alt="Profile"
                className="h-10 w-10 rounded-full object-cover"
              />
            </button>

            {isProfileOpen && (
              <div className="absolute right-0 top-14 z-50 w-52 rounded-xl border border-white/60 bg-white/60 p-2 shadow-xl backdrop-blur-xl">
                <button
                  type="button"
                  className="w-full rounded-lg px-4 py-3 text-left text-sm font-medium text-slate-800 transition hover:bg-white/60"
                  onClick={() => {
                    setIsProfileOpen(false)
                  }}
                >
                  History
                </button>

                <button
                  type="button"
                  className="w-full rounded-lg px-4 py-3 text-left text-sm font-medium text-slate-800 transition hover:bg-white/60"
                  onClick={() => {
                    setIsProfileOpen(false)
                  }}
                >
                  Document Verification
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {apiError && (
        <div className="px-4 pt-4 sm:px-6 lg:px-8">
          <div className="mx-auto flex w-full max-w-7xl items-center justify-between gap-4 rounded-xl border border-red-200/60 bg-red-50/60 px-4 py-3 text-sm text-red-700 shadow-sm backdrop-blur-md">
            <span className="min-w-0 break-words">
              Backend error: {apiError}
            </span>

            <button
              onClick={() => setApiError(null)}
              aria-label="dismiss"
              className="shrink-0 rounded-lg border border-red-200/60 bg-white/50 px-3 py-1.5 text-xs font-medium text-red-700 backdrop-blur-md transition hover:bg-white/80"
            >
              Clear
            </button>
          </div>
        </div>
      )}

      <main className="mx-auto w-full max-w-7xl px-4 py-5 sm:px-6 sm:py-7 lg:px-8">
        <div className="grid grid-cols-1 gap-5 xl:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
          <div className="min-w-0 space-y-5">
            <InputPanel
              value={sourceContent}
              onChange={setSourceContent}
            />

            <OutputTypeSelector
              selected={selectedOutputs}
              onToggle={toggleOutput}
            />

            <ParametersPanel
              params={params}
              onChange={setParams}
            />

            <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
              <button
                className="w-full rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-slate-900/10 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:text-slate-500 sm:w-auto"
                onClick={handleGenerate}
                disabled={!canGenerate()}
              >
                {loading ? 'Generating...' : 'Generate Content'}
              </button>

              <div className="text-xs text-slate-500">
                {!sourceContent.trim() && (
                  <span></span>
                )}

                {sourceContent.trim() &&
                  selectedOutputs.length === 0 && (
                    <span>Select at least one output type</span>
                  )}
              </div>
            </div>
          </div>

          <div className="min-w-0 xl:sticky xl:top-5 xl:self-start">
            <OutputPanel
              results={results}
              loading={loading}
              currentType={currentType}
            />
          </div>
        </div>
      </main>

     
    </div>
  )
}
