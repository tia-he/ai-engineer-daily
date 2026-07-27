export default function NewsCardSkeleton() {
  return (
    <div className="animate-pulse rounded-3xl border border-gray-200 bg-white p-7">
      <div className="flex gap-6">
        <div className="h-4 w-6 rounded bg-gray-200" />

        <div className="min-w-0 flex-1 space-y-3">
          <div className="h-6 w-3/4 rounded bg-gray-200" />
          <div className="h-4 w-full rounded bg-gray-100" />
          <div className="h-4 w-2/3 rounded bg-gray-100" />
          <div className="mt-2 h-4 w-24 rounded bg-gray-200" />
        </div>
      </div>
    </div>
  );
}
