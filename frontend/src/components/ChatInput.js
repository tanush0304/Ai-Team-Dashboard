import {
  HStack,
  IconButton,
  Input,
  InputGroup,
  InputRightElement,
} from "@chakra-ui/react";

import { FiSend } from "react-icons/fi";

function ChatInput({
  value,
  onChange,
  onSend,
  loading,
}) {
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !loading) {
      onSend(e);
    }
  };

  return (
    <HStack
      spacing={3}
      w="100%"
      mt={4}
    >
      <InputGroup size="lg">

        <Input
          placeholder="Ask AI anything about your dashboard..."
          value={value}
          onChange={onChange}
          onKeyDown={handleKeyDown}
          bg="white"
          borderRadius="full"
          border="1px solid"
          borderColor="gray.300"
          _focus={{
            borderColor: "blue.400",
            boxShadow: "0 0 0 1px #3182CE",
          }}
        />

        <InputRightElement mr={2}>
          <IconButton
            aria-label="Send"
            icon={<FiSend />}
            colorScheme="blue"
            borderRadius="full"
            size="sm"
            isLoading={loading}
            onClick={onSend}
          />
        </InputRightElement>

      </InputGroup>
    </HStack>
  );
}

export default ChatInput;