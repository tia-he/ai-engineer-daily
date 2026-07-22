import { ReactNode } from "react";

type SectionProps = {
  title: string;
  children: ReactNode;
};

export default function Section({
  title,
  children,
}: SectionProps) {
  return (
    <section className="mt-14">
      <h2 className="text-2xl font-semibold tracking-tight text-gray-900">
        {title}
      </h2>

      <div className="mt-6">
        {children}
      </div>
    </section>
  );
}