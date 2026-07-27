import React, { useEffect, useRef, useState } from "react";

import {
  Box,
  Button,
  Flex,
  Heading,
  HStack,
  Spinner,
  Text,
  useDisclosure,
  VStack,
} from "@chakra-ui/react";

import { FiClock } from "react-icons/fi";

import {
  sendChatMessage,
  getChatHistory,
} from "../api/api";

import ChatMessage from "../components/ChatMessage";
import ChatInput from "../components/ChatInput";
import QuickPrompts from "../components/QuickPrompts";
import SqlAccordion from "../components/SqlAccordion";
import ChatHistoryDrawer from "../components/ChatHistoryDrawer";

function AIAssistant() {
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "👋 Hello! I'm your AI Team Assistant. Ask me anything about your dashboard.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [history, setHistory] = useState([]);

  const [latestSql, setLatestSql] = useState("");

  const bottomRef = useRef(null);

  const {
    isOpen,
    onOpen,
    onClose,
  } = useDisclosure();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const loadHistory = async () => {
    try {
      const res = await getChatHistory();
      setHistory(res.history || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const question = input;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: question,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const data = await sendChatMessage(question);

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text:
            data.response ||
            "No response received.",
        },
      ]);

      if (data.sql) {
        setLatestSql(data.sql);
      } else {
        setLatestSql("");
      }

      loadHistory();
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "Something went wrong while contacting the AI.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handlePrompt = (prompt) => {
    setInput(prompt);
  };

  const handleLoadChat = (chat) => {
    setMessages([
      {
        sender: "user",
        text: chat.question,
      },
      {
        sender: "ai",
        text: chat.ai_response,
      },
    ]);

    onClose();
  };

  useEffect(() => {
    loadHistory();
  }, []);

    return (
    <>
      <Flex
        justify="space-between"
        align="center"
        mb={6}
      >
        <Box>
          <Heading size="lg">
            AI Team Assistant
          </Heading>

          <Text
            color="gray.500"
            mt={1}
          >
            Ask questions about your team, projects and daily updates.
          </Text>
        </Box>

        <Button
          leftIcon={<FiClock />}
          colorScheme="blue"
          variant="outline"
          onClick={onOpen}
        >
          Chat History
        </Button>
      </Flex>

      <QuickPrompts
        onSelect={handlePrompt}
      />

      <Box
        mt={6}
        bg="white"
        borderRadius="xl"
        border="1px solid"
        borderColor="gray.200"
        h="520px"
        overflowY="auto"
        p={5}
      >
        <VStack
          spacing={4}
          align="stretch"
        >
          {messages.map((msg, index) => (
            <ChatMessage
              key={index}
              sender={msg.sender}
              text={msg.text}
            />
          ))}

          {loading && (
            <Flex
              align="center"
              gap={3}
            >
              <Spinner size="sm" />

              <Text color="gray.500">
                AI is thinking...
              </Text>
            </Flex>
          )}

          <div ref={bottomRef} />
        </VStack>
      </Box>

      {latestSql && (
        <SqlAccordion
          sql={latestSql}
        />
      )}

      <ChatInput
        value={input}
        onChange={(e) =>
          setInput(e.target.value)
        }
        onSend={handleSend}
        loading={loading}
      />

      <ChatHistoryDrawer
        isOpen={isOpen}
        onClose={onClose}
        history={history}
        loading={loading}
        onLoadChat={handleLoadChat}
      />
    </>
  );
}

export default AIAssistant;