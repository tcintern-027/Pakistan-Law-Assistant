import { useState } from "react";
import Header from "./components/layout/Header";
import Sidebar from "./components/layout/Sidebar";
import MessageInput from "./components/chat/MessageInput";
import MessageList from "./components/chat/MessageList";
import WelcomeScreen from "./components/chat/WelcomeScreen";
import { askQuestion } from "./services/api";
import type { Message } from "./components/chat/MessageList";

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleQuestion = async (question: string) => {
    if (isLoading) {
      return;
    }

    const userMessage: Message = {
      id: Date.now(),
      role: "user",
      content: question,
    };

    const loadingMessage: Message = {
      id: Date.now() + 1,
      role: "assistant",
      content: "",
      loading: true,
    };

    setMessages((current) => [
      ...current,
      userMessage,
      loadingMessage,
    ]);

    setIsLoading(true);

    try {
      const result = await askQuestion(question);

      setMessages((current) =>
        current.map((message) =>
          message.id === loadingMessage.id
            ? {
                id: loadingMessage.id,
                role: "assistant",
                content: result.answer,
                sources: result.sources,
              }
            : message,
        ),
      );
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Something went wrong while contacting the server.";

      setMessages((current) =>
        current.map((message) =>
          message.id === loadingMessage.id
            ? {
                id: loadingMessage.id,
                role: "assistant",
                content: `Unable to get an answer.\n\n${errorMessage}`,
              }
            : message,
        ),
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] text-white">
      <Header />

      <main className="mx-auto flex min-h-[calc(100vh-4rem)] max-w-7xl">
        <Sidebar />

        <section className="flex min-w-0 flex-1 flex-col">
          {messages.length === 0 ? (
            <WelcomeScreen onSuggestionClick={handleQuestion} />
          ) : (
            <div className="flex-1 overflow-y-auto">
              <MessageList messages={messages} />
            </div>
          )}

          <MessageInput onSubmit={handleQuestion} />
        </section>
      </main>
    </div>
  );
}

export default App;