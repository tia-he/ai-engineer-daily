import { ReactNode } from "react";

type SectionProps = {
  title: string;
  /** Short factual note beside the heading — counts, provenance, timing. */
  meta?: string;
  children: ReactNode;
};

export default function Section({ title, meta, children }: SectionProps) {
  return (
    <section className="mt-12">
      <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 border-b border-rule pb-4">
        <h2 className="text-2xl font-semibold tracking-tight text-ink">
          {title}
        </h2>

        {meta ? (
          <span className="shrink-0 font-mono text-xs uppercase tracking-[0.14em] text-ink-faint">
            {meta}
          </span>
        ) : null}
      </div>

      <div className="mt-6">{children}</div>
    </section>
  );
}
