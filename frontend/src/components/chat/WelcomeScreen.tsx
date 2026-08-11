import { Scale } from "lucide-react";

interface WelcomeScreenProps {
  onSuggestionClick: (question: string) => void;
}

const suggestions = [
  {
    question: "What does Article 10A provide?",
    document: "Constitution of Pakistan",
  },
  {
    question: "What is Section 302?",
    document: "Pakistan Penal Code",
  },
  {
    question: "What does PECA say about real-time collection of information?",
    document: "PECA",
  },
  {
    question: "What does the Contract Act say about agreements?",
    document: "Contract Act, 1872",
  },
];

function WelcomeScreen({ onSuggestionClick }: WelcomeScreenProps) {
  return (
    <div className="flex flex-1 items-center justify-center px-6 py-12">
      <div className="w-full max-w-3xl text-center">
        <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-2xl border border-blue-500/20 bg-blue-500/10 text-blue-400">
          <Scale size={28} />
        </div>

        <h2 className="text-3xl font-semibold tracking-tight">
          Ask about Pakistani law
        </h2>

        <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-gray-500">
          Ask questions about the Constitution of Pakistan, Pakistan Penal
          Code, Contract Act, PECA, and other indexed legal documents.
        </p>

        <div className="mt-8 grid gap-3 sm:grid-cols-2">
          {suggestions.map((suggestion) => (
            <button
              key={suggestion.question}
              type="button"
              onClick={() => onSuggestionClick(suggestion.question)}
              className="rounded-xl border border-white/10 bg-white/[0.02] p-4 text-left transition hover:border-white/20 hover:bg-white/[0.04]"
            >
              <p className="text-sm font-medium">{suggestion.question}</p>

              <p className="mt-1 text-xs text-gray-500">
                {suggestion.document}
              </p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default WelcomeScreen;