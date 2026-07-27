import {
  Avatar,
  Box,
  Flex,
  Text,
} from "@chakra-ui/react";

function ChatMessage({ sender, text }) {
  const isUser = sender === "user";

  return (
    <Flex justify={isUser ? "flex-end" : "flex-start"}>
      <Flex
        maxW="80%"
        align="flex-start"
        gap={3}
        flexDir={isUser ? "row-reverse" : "row"}
      >
        <Avatar
          size="sm"
          name={isUser ? "You" : "AI"}
          bg={isUser ? "blue.500" : "purple.500"}
        />

        <Box
          bg={isUser ? "blue.500" : "gray.100"}
          color={isUser ? "white" : "black"}
          px={4}
          py={3}
          borderRadius="xl"
        >
          <Text whiteSpace="pre-wrap">
            {text}
          </Text>
        </Box>
      </Flex>
    </Flex>
  );
}

export default ChatMessage;