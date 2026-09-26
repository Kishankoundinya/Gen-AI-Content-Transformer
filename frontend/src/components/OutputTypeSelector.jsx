
import React from 'react'

const OUTPUT_TYPES = [
  {
    name: 'Video',
    description: 'Script, storyboard, scenes, narration, subtitles and visuals',
  },
  {
    name: 'LinkedIn Post',
    description: 'Professional post ready to publish',
  },
  {
    name: 'Twitter/X Post',
    description: 'Single tweet, thread and engagement tweet',
  },
  {
    name: 'Advisory',
    description: 'Structured advisory with recommendations',
  },
  {
    name: 'Infographic',
    description: 'Content, layout and key messaging',
  },
  {
    name: 'Executive Summary',
    description: 'Concise executive briefing',
  },
  {
    name: 'Presentation',
    description: 'Slides with speaker notes and design tips',
  },
]

export default function OutputTypeSelector({ selected, onToggle }) {
  return (
    <section className="rounded-2xl border border-white/40 bg-white/55 shadow-[0_8px_32px_rgba(15,23,42,0.08)] backdrop-blur-xl">
      <div className="flex flex-col gap-1 border-b border-white/40 px-4 py-4 sm:px-5">
        <div className="flex items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-semibold tracking-tight text-slate-900 sm:text-lg">
              Output Types
            </h2>

            <p className="mt-1 text-xs text-slate-500 sm:text-sm">
              Select one or more formats
            </p>
          </div>

          {selected.length > 0 && (
            <span className="shrink-0 rounded-full border border-white/50 bg-white/50 px-3 py-1 text-xs font-medium text-slate-600 backdrop-blur-md">
              {selected.length} selected
            </span>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-3 p-4 sm:grid-cols-2 sm:p-5 lg:grid-cols-3">
        {OUTPUT_TYPES.map((type) => {
          const active = selected.includes(type.name)

          return (
            <button
              key={type.name}
              type="button"
              className={`rounded-xl border p-4 text-left backdrop-blur-md transition-all duration-200 ${
                active
                  ? 'border-slate-400/70 bg-slate-900/90 text-white shadow-lg shadow-slate-900/10'
                  : 'border-white/50 bg-white/35 text-slate-800 hover:border-white/80 hover:bg-white/60'
              }`}
              onClick={() => onToggle(type.name)}
              aria-pressed={active}
            >
              <div className="flex items-center justify-between gap-3">
                <span className="text-sm font-semibold">
                  {type.name}
                </span>

                {active && (
                  <span className="text-xs font-medium text-white/80">
                    Selected
                  </span>
                )}
              </div>

              <span
                className={`mt-2 block text-xs leading-5 ${
                  active ? 'text-white/70' : 'text-slate-500'
                }`}
              >
                {type.description}
              </span>
            </button>
          )
        })}
      </div>
    </section>
  )
}

