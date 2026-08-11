import { ArrowUp } from "lucide-react";
import { useState } from "react";
import type { FormEvent } from "react";

interface MessageInputProps {
  onSubmit: (question: string) => void;
}

function MessageInput({ onSubmit }: MessageInputProps) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) {
      return;
    }

    onSubmit(trimmedQuestion);
    setQuestion("");
  };

  return (
    <div className="border-t border-white/10 p-5">
      <form
        onSubmit={handleSubmit}
        className="mx-auto flex max-w-3xl items-end gap-3 rounded-2xl border border-white/10 bg-[#111827] p-3 shadow-2xl"
      >
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              event.currentTarget.form?.requestSubmit();
            }
          }}
          rows={1}
          placeholder="Ask a legal question..."
          className="min-h-12 flex-1 resize-none bg-transparent px-3 py-3 text-sm text-gray-100 outline-none placeholder:text-gray-600"
        />

        <button
          type="submit"
          disabled={!question.trim()}
          className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600 text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-40"
          aria-label="Send question"
        >
          <ArrowUp size={19} />
        </button>
      </form>

      <p className="mx-auto mt-3 max-w-3xl text-center text-xs text-gray-600">
        Educational information only. Not a substitute for professional legal
        advice.
      </p>
    </div>
  );
}

export default MessageInput;