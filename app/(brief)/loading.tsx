export default function Loading() {
  return (
    <main>
      <div className="chrome-grid animate-pulse border-b border-white/10 bg-chrome">
        <div className="mx-auto w-full max-w-3xl px-6 py-16 sm:py-20">
          <div className="h-3 w-48 rounded-full bg-white/10" />
          <div className="mt-5 h-12 w-2/3 rounded-full bg-white/10" />
          <div className="mt-5 h-5 w-1/2 rounded-full bg-white/10" />
        </div>
      </div>

      <div className="mx-auto w-full max-w-3xl px-6 pb-20 pt-12">
        <div className="animate-pulse space-y-5">
          {[0, 1, 2].map((row) => (
            <div
              key={row}
              className="flex flex-col gap-5 rounded-3xl border border-rule bg-card p-7 shadow-sm sm:flex-row sm:gap-6"
            >
              <div className="h-40 w-full shrink-0 rounded-2xl bg-accent-soft sm:h-32 sm:w-32" />

              <div className="min-w-0 flex-1">
                <div className="h-3 w-24 rounded-full bg-accent-soft" />
                <div className="mt-5 h-6 w-3/4 rounded-full bg-accent-soft" />
                <div className="mt-4 h-4 w-full rounded-full bg-accent-soft" />
                <div className="mt-2 h-4 w-2/3 rounded-full bg-accent-soft" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
