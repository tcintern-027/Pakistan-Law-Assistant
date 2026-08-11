import { FileText } from "lucide-react";

const documents = [
  "Constitution of Pakistan",
  "Pakistan Penal Code",
  "Contract Act, 1872",
  "PECA",
];

function DocumentList() {
  return (
    <div className="space-y-2">
      {documents.map((document) => (
        <div
          key={document}
          className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-gray-400 transition hover:bg-white/5 hover:text-gray-200"
        >
          <FileText size={16} />
          <span>{document}</span>
        </div>
      ))}
    </div>
  );
}

export default DocumentList;