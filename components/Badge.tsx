type BadgeProps = {
  text: string;
};

export default function Badge({ text }: BadgeProps) {
  return (
    <span className="rounded-full border border-gray-200 bg-gray-100 px-3.5 py-1.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-200">
      {text}
    </span>
  );
}