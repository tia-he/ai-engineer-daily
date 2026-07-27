import { ReactNode } from "react";

type EmptyStateProps = {
  icon: ReactNode;
  title: string;
  description: string;
};

export default function EmptyState({ icon, title, description }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center rounded-3xl border border-gray-200 bg-white px-8 py-16 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gray-100 text-gray-400">
        {icon}
      </div>

      <h3 className="mt-6 text-xl font-semibold text-gray-900">{title}</h3>

      <p className="mt-2 max-w-sm text-gray-600">{description}</p>
    </div>
  );
}
