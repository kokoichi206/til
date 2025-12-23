import React, { useEffect, useState } from "react";
import { Box, render, Text } from "ink";
import { ModelMessage, streamText } from "ai";
import Spinner from "ink-spinner";
import TextInput from "ink-text-input";
import { createOpenRouter } from "@openrouter/ai-sdk-provider";

const App = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ModelMessage[]>([]);
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (input.trim() === "") return;
    setInput("");
    const res = await generateResponse(input);
    setMessages((prev) => [
      ...prev,
      { role: "user", content: input },
      { role: "assistant", content: res },
    ]);
  };

  const openrouter = createOpenRouter({
    apiKey: process.env.OPEN_ROUTER_API_KEY,
  });

  const generateResponse = async (prompt: string): Promise<string> => {
    setLoading(true);
    const res = streamText({
      model: openrouter.chat("openai/gpt-5-mini"),
      messages: [...messages, { role: "user", content: prompt }],
    });

    let fullResponse = "";
    for await (const chunk of res.textStream) {
      setLoading(false);
      setResponse((prev) => prev + chunk);
      fullResponse += chunk;
    }
    setResponse("");

    return fullResponse;
  };

  return (
    <Box flexDirection="column">
      {messages.map((message, index) => (
        <Text key={index} color={message.role === "user" ? "green" : "white"}>
          {message.role}:{" "}
          {typeof message.content === "string" ? message.content : ""}
        </Text>
      ))}
      {loading && (
        <Text color="yellow">
          <Spinner type="dots" /> Loading...
        </Text>
      )}
      <Text color="white">{response}</Text>

      <Box marginRight={1} borderColor="gray" borderStyle="round">
        <Text color="white">{">"} </Text>
        <TextInput
          value={input}
          onChange={(input) => {
            setInput(input);
          }}
          onSubmit={() => handleSubmit()}
          placeholder="Type your message here..."
        />
      </Box>
    </Box>
  );
};

render(<App />);
