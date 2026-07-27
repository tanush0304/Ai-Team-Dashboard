import {
  Avatar,
  Badge,
  Box,
  Button,
  Divider,
  Drawer,
  DrawerBody,
  DrawerCloseButton,
  DrawerContent,
  DrawerHeader,
  DrawerOverlay,
  HStack,
  Input,
  InputGroup,
  InputLeftElement,
  Spinner,
  Text,
  VStack,
} from "@chakra-ui/react";

import {
  FiClock,
  FiSearch,
} from "react-icons/fi";

import { useMemo, useState } from "react";

function ChatHistoryDrawer({
  isOpen,
  onClose,
  history,
  loading,
  onLoadChat,
}) {
  const [search, setSearch] = useState("");

  const filteredHistory = useMemo(() => {
    if (!search.trim()) return history;

    return history.filter((item) => {
      return (
        item.question
          ?.toLowerCase()
          .includes(search.toLowerCase()) ||
        item.ai_response
          ?.toLowerCase()
          .includes(search.toLowerCase())
      );
    });
  }, [history, search]);

  return (
    <Drawer
      isOpen={isOpen}
      placement="right"
      onClose={onClose}
      size="md"
    >
      <DrawerOverlay />

      <DrawerContent>

        <DrawerCloseButton />

        <DrawerHeader
          borderBottomWidth="1px"
        >
          AI Chat History
        </DrawerHeader>

        <DrawerBody>

          <InputGroup mb={5}>
            <InputLeftElement>
              <FiSearch />
            </InputLeftElement>

            <Input
              placeholder="Search previous chats..."
              value={search}
              onChange={(e) =>
                setSearch(e.target.value)
              }
            />
          </InputGroup>

          {loading ? (
            <Spinner />
          ) : filteredHistory.length === 0 ? (
            <Text
              color="gray.500"
            >
              No previous chats found.
            </Text>
          ) : (
            <VStack
              spacing={4}
              align="stretch"
            >
              {filteredHistory.map((chat) => (
                <Box
                  key={chat.id}
                  bg="gray.50"
                  p={4}
                  borderRadius="xl"
                  border="1px solid"
                  borderColor="gray.200"
                  transition=".2s"
                  _hover={{
                    boxShadow: "md",
                  }}
                >
                  <HStack
                    justify="space-between"
                    mb={3}
                  >
                    <Badge
                      colorScheme="blue"
                    >
                      Question
                    </Badge>

                    <HStack
                      spacing={1}
                    >
                      <FiClock />

                      <Text
                        fontSize="xs"
                        color="gray.500"
                      >
                        {new Date(
                          chat.created_at
                        ).toLocaleDateString()}
                      </Text>
                    </HStack>
                  </HStack>

                  <Text
                    fontWeight="bold"
                    mb={3}
                  >
                    {chat.question}
                  </Text>

                  <Divider mb={3} />

                  <HStack
                    align="start"
                  >
                    <Avatar
                      size="xs"
                      bg="purple.500"
                      name="AI"
                    />

                    <Text
                      noOfLines={4}
                      color="gray.600"
                      fontSize="sm"
                    >
                      {chat.ai_response}
                    </Text>
                  </HStack>

                  <Button
                    mt={4}
                    size="sm"
                    colorScheme="blue"
                    variant="outline"
                    w="full"
                    onClick={() =>
                      onLoadChat(chat)
                    }
                  >
                    Load Conversation
                  </Button>
                </Box>
              ))}
            </VStack>
          )}
        </DrawerBody>
      </DrawerContent>
    </Drawer>
  );
}

export default ChatHistoryDrawer;