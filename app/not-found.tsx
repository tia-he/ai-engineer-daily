import Link from "next/link";

export default function NotFound() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 px-6 text-center">
      <p className="text-sm font-semibold uppercase tracking-[0.2em] text-gray-500">
        404
      </p>

      <h1 className="mt-4 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
        Story not found
      </h1>

      <p className="mt-4 max-w-md text-lg text-gray-600">
        This article may have been removed, or the link is incorrect.
      </p>

      <Link
        href="/"
        className="mt-8 inline-flex items-center rounded-full bg-gray-900 px-6 py-3 text-sm font-semibold text-white transition-all duration-300 hover:bg-gray-700 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-900 focus-visible:ring-offset-2"
      >
        ← Back to Today&apos;s Brief
      </Link>
    </main>
  );
}
