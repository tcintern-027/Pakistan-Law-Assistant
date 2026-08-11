export interface Source {
  source: string;
  page: number | null;
  chunk_id?: string;
  chunk_index?: number;
}

export interface AskResponse {
  question: string;
  answer: string;
  sources: Source[];
}

const API_BASE_URL = "http://127.0.0.1:8000";

export async function askQuestion(
  question: string,
): Promise<AskResponse> {
  const response = await fetch(`${API_BASE_URL}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
    }),
  });

  if (!response.ok) {
    let message = "Failed to get a response from the server.";

    try {
      const error = await response.json();

      if (error.detail) {
        message =
          typeof error.detail === "string"
            ? error.detail
            : "The server rejected the request.";
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  return response.json();
}