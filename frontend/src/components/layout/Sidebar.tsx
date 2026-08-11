import { BookOpen } from "lucide-react";
import DocumentList from "../documents/DocumentList";

function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 border-r border-white/10 p-5 lg:block">
      <div className="mb-6 flex items-center gap-2 text-sm font-medium">
        <BookOpen size={17} />
        Legal Documents
      </div>

      <DocumentList />
    </aside>
  );
}

export default Sidebar;