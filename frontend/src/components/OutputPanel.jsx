
import React from 'react'

function formatFileName(type) {
  return type
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '')
}

export default function OutputPanel({ results, loading, currentType }) {
  const successful = results.filter((r) => r.status === 'success')
  const failed = results.filter((r) => r.status !== 'success')

  return (
    <section className="flex min-h-[450px] flex-col overflow-hidden rounded-2xl border border-white/40 bg-white/55 shadow-[0_8px_32px_rgba(15,23,42,0.08)] backdrop-blur-xl">
      <div className="border-b border-white/40 px-4 py-4 sm:px-5">
        <div className="flex items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-semibold tracking-tight text-slate-900 sm:text-lg">
              Generated Content
            </h2>

            <p className="mt-1 text-xs text-slate-500 sm:text-sm">
              {loading
                ? `Generating ${currentType || ''}...`
                : `${successful.length} output(s) ready`}
            </p>
          </div>

          {successful.length > 0 && !loading && (
            <span className="rounded-full border border-white/50 bg-white/50 px-3 py-1 text-xs font-medium text-slate-600 backdrop-blur-md">
              {successful.length} ready
            </span>
          )}
        </div>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto p-4 sm:p-5">
        {!loading && results.length === 0 && (
          <div className="flex min-h-[350px] items-center justify-center rounded-xl border border-dashed border-slate-300/60 bg-white/20 px-6 text-center backdrop-blur-md">
            <div className="max-w-sm">
              <h3 className="text-base font-semibold text-slate-700">
                No content generated yet
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-500">
                Add your source content, select output types, then click
                Generate Content. Results will appear here.
              </p>
            </div>
          </div>
        )}

        {loading && (
          <div className="rounded-xl border border-white/50 bg-white/30 p-5 backdrop-blur-md sm:p-6">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-semibold text-slate-800">
                  Generating content
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  {currentType
                    ? `Generating ${currentType}...`
                    : 'Preparing...'}
                </p>
              </div>

              <div className="h-7 w-7 shrink-0 animate-spin rounded-full border-2 border-slate-300 border-t-slate-800" />
            </div>

            <div className="mt-5 h-1.5 overflow-hidden rounded-full bg-slate-200/70">
              <div className="h-full w-1/2 animate-pulse rounded-full bg-slate-700" />
            </div>

            <p className="mt-3 text-xs leading-5 text-slate-500">
              This can take 10-60 seconds on CPU.
            </p>
          </div>
        )}

        {!loading && successful.length > 0 && (
          <div className="space-y-3">
            {successful.map((result) => (
              <details
                className="overflow-hidden rounded-xl border border-white/50 bg-white/30 backdrop-blur-md"
                key={result.output_type}
                open={successful.length === 1}
              >
                <summary className="flex cursor-pointer list-none items-center justify-between gap-3 border-b border-white/40 bg-white/30 px-4 py-3.5 transition hover:bg-white/50 sm:px-5">
                  <span className="min-w-0 truncate text-sm font-semibold text-slate-800">
                    {result.output_type}
                  </span>

                  <a
                    className="shrink-0 rounded-lg border border-white/60 bg-white/50 px-3 py-1.5 text-xs font-medium text-slate-700 backdrop-blur-md transition hover:bg-white/80"
                    href={`data:text/markdown;charset=utf-8,${encodeURIComponent(
                      result.content,
                    )}`}
                    download={`${formatFileName(result.output_type)}.md`}
                    onClick={(e) => e.stopPropagation()}
                    title={`Download ${result.output_type} as Markdown`}
                  >
                    Download
                  </a>
                </summary>

                <pre className="max-h-[500px] overflow-auto whitespace-pre-wrap break-words bg-white/20 p-4 font-mono text-xs leading-6 text-slate-700 sm:p-5 sm:text-sm">
                  {result.content}
                </pre>
              </details>
            ))}
          </div>
        )}

        {failed.length > 0 && (
          <div className="mt-3 space-y-2">
            {failed.map((r) => (
              <p
                className="rounded-xl border border-red-200/60 bg-red-50/50 px-4 py-3 text-sm text-red-700 backdrop-blur-md"
                key={r.output_type}
              >
                <strong>{r.output_type}:</strong> {r.status}
              </p>
            ))}
          </div>
        )}
      </div>

      {!loading && successful.length > 1 && (
        <div className="border-t border-white/40 bg-white/25 p-4 backdrop-blur-md sm:p-5">
          <button
            className="w-full rounded-xl border border-slate-800/20 bg-slate-900 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-slate-900/10 transition hover:bg-slate-800"
            onClick={() => {
              const blob = successful
                .map(
                  (r) =>
                    `# ${r.output_type}\n\n${r.content}\n\n---\n\n`,
                )
                .join('')

              const url = URL.createObjectURL(
                new Blob([blob], { type: 'text/markdown' }),
              )

              const link = document.createElement('a')
              link.href = url
              link.download = 'all_outputs.md'
              link.click()
              URL.revokeObjectURL(url)
            }}
          >
            Download All as Markdown
          </button>
        </div>
      )}
    </section>
  )
}

