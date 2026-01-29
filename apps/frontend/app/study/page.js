import { Suspense } from "react";
import StudyClient from "./StudyClient";

export default function StudyPage() {
  return (
    <Suspense fallback={<div className="p-6">Loading study page…</div>}>
      <StudyClient />
    </Suspense>
  );
}
