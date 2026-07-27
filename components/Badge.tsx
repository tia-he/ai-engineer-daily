type BadgeProps = {
  text: string;
};

export default function Badge({ text }: BadgeProps) {
  // Non-interactive by design: these label a story, they don't filter it.
  // No hover state, so nothing here reads as a button.
  return (
    <span className="rounded-full border border-rule bg-accent-soft px-3 py-1 font-mono text-xs tracking-tight text-ink-muted">
      {text}
    </span>
  );
}
