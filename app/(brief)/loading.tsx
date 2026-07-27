export default function Loading() {
  return (
    <main className="px-6 pb-20 pt-16">
      <div className="mx-auto w-full max-w-3xl animate-pulse">
        <div className="h-3 w-48 rounded-full bg-accent-soft" />
        <div className="mt-5 h-12 w-2/3 rounded-full bg-accent-soft" />
        <div className="mt-5 h-5 w-1/2 rounded-full bg-accent-soft" />

        <div className="mt-12 space-y-5">
          {[0, 1, 2].map((row) => (
            <div
              key={row}
              className="rounded-3xl border border-rule bg-card p-7 shadow-sm"
            >
              <div className="h-3 w-24 rounded-full bg-accent-soft" />
              <div className="mt-5 h-6 w-3/4 rounded-full bg-accent-soft" />
              <div className="mt-4 h-4 w-full rounded-full bg-accent-soft" />
              <div className="mt-2 h-4 w-2/3 rounded-full bg-accent-soft" />
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
