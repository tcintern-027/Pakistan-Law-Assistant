import type { Source } from "../../services/api";

export interface Message {
  id: number;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  loading?: boolean;
}

interface MessageListProps {
  messages: Message[];
}

function MessageList({ messages }: MessageListProps) {
  return (
    <div className="mx-auto w-full max-w-3xl space-y-6 px-6 py-8">
      {messages.map((message) => (
        <div
          key={message.id}
          className={
            message.role === "user"
              ? "flex justify-end"
              : "flex justify-start"
          }
        >
          <div className="max-w-[90%]">
            <div
              className={
                message.role === "user"
                  ? "rounded-2xl rounded-br-md bg-blue-600 px-4 py-3 text-sm leading-6"
                  : "rounded-2xl rounded-bl-md border border-white/10 bg-[#111827] px-5 py-4 text-sm leading-6 text-gray-300"
              }
            >
              {message.loading ? (
                <div className="flex items-center gap-2 text-gray-400">
                  <span className="h-2 w-2 animate-pulse rounded-full bg-gray-500" />
                  <span className="h-2 w-2 animate-pulse rounded-full bg-gray-500 [animation-delay:150ms]" />
                  <span className="h-2 w-2 animate-pulse rounded-full bg-gray-500 [animation-delay:300ms]" />
                </div>
              ) : (
                <div className="whitespace-pre-wrap">
                  {message.content}
                </div>
              )}
            </div>

            {message.role === "assistant" &&
              message.sources &&
              message.sources.length > 0 && (
                <div className="mt-3 rounded-xl border border-white/10 bg-white/[0.02] p-4">
                  <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-gray-500">
                    Sources
                  </p>

                  <div className="space-y-2">
                    {message.sources.map((source, index) => (
                      <div
                        key={`${source.source}-${source.page}-${index}`}
                        className="flex items-center justify-between gap-4 rounded-lg bg-white/[0.02] px-3 py-2 text-xs"
                      >
                        <span className="truncate text-gray-400">
                          {source.source}
                        </span>

                        {source.page !== null && (
                          <span className="shrink-0 text-gray-500">
                            Page {source.page}
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
          </div>
        </div>
      ))}
    </div>
  );
}

export default MessageList;