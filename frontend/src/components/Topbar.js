import {
  Flex,
  Heading,
  Spacer,
  Avatar,
  Text,
  HStack,
  Input,
  InputGroup,
  InputLeftElement,
  Icon,
  Badge,
} from "@chakra-ui/react";

import {
  FiSearch,
  FiBell,
} from "react-icons/fi";

function Topbar() {
  return (
    <Flex
      bg="white"
      px={8}
      py={5}
      align="center"
      borderBottom="1px solid"
      borderColor="gray.200"
      position="sticky"
      top="0"
      zIndex="100"
    >
      <Heading
          size="md"
          bgGradient="linear(to-r, blue.500, purple.500)"
          bgClip="text"
      >
        AI Team Dashboard
      </Heading>

      <Spacer />

      <InputGroup
        maxW="320px"
        mr={6}
      >
        <InputLeftElement>
          <Icon as={FiSearch} color="gray.400" />
        </InputLeftElement>

        <Input
          placeholder="Search..."
          bg="gray.50"
          borderRadius="full"
        />
      </InputGroup>

      <HStack spacing={6}>
        <Badge
          colorScheme="blue"
          borderRadius="full"
          px={3}
          py={1}
        >
          AI Ready
        </Badge>

        <Icon
          as={FiBell}
          fontSize="22px"
          color="gray.600"
          cursor="pointer"
        />

        <HStack>
          <Avatar
            size="sm"
            name="Tanush"
            bg="blue.500"
          />

          <Text
            fontWeight="600"
            color="gray.700"
          >
            Tanush
          </Text>
        </HStack>
      </HStack>
    </Flex>
  );
}

export default Topbar;