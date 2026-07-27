import {
  Avatar,
  Badge,
  Box,
  Divider,
  Flex,
  Heading,
  HStack,
  Icon,
  Progress,
  Text,
  VStack,
} from "@chakra-ui/react";

import {
  FiAward,
  FiClock,
} from "react-icons/fi";

function TopContributor({ updates, members }) {

  const totals = {};

  updates.forEach((update) => {
    totals[update.member_id] =
      (totals[update.member_id] || 0) +
      Number(update.hours_worked);
  });

  let topId = null;
  let maxHours = 0;

  Object.keys(totals).forEach((id) => {
    if (totals[id] > maxHours) {
      maxHours = totals[id];
      topId = Number(id);
    }
  });

  const member = members.find(
    (m) => m.id === topId
  );

  if (!member) {
    return null;
  }

  const completedTasks = updates.filter(
    (u) =>
      u.member_id === topId &&
      u.status === "Completed"
  ).length;

  return (
    <Box
      bg="white"
      borderRadius="2xl"
      p={6}
      boxShadow="sm"
      border="1px solid"
      borderColor="gray.100"
      transition=".3s"
      _hover={{
        transform: "translateY(-4px)",
        boxShadow: "xl",
      }}
    >
      <Flex
        justify="space-between"
        align="center"
        mb={5}
      >
        <Heading
          size="md"
          color="gray.700"
        >
          🏆 Top Contributor
        </Heading>

        <Badge
          colorScheme="yellow"
          px={3}
          py={1}
          borderRadius="full"
        >
          MVP
        </Badge>
      </Flex>

      <Divider mb={5} />

      <HStack spacing={5} align="center">

        <Avatar
          size="xl"
          name={member.full_name}
          bg="blue.500"
        />

        <VStack
          align="start"
          spacing={2}
          flex="1"
        >
          <Text
            fontSize="xl"
            fontWeight="bold"
          >
            {member.full_name}
          </Text>

          <Text color="gray.500">
            Highest contributor this week
          </Text>

          <Progress
            value={100}
            size="sm"
            colorScheme="blue"
            borderRadius="full"
            w="100%"
          />

          <HStack spacing={6}>

            <HStack>
              <Icon
                as={FiClock}
                color="orange.400"
              />
              <Text
                fontWeight="600"
              >
                {maxHours} hrs
              </Text>
            </HStack>

            <HStack>
              <Icon
                as={FiAward}
                color="green.500"
              />
              <Text
                fontWeight="600"
              >
                {completedTasks} Tasks
              </Text>
            </HStack>

          </HStack>

        </VStack>

      </HStack>

    </Box>
  );
}

export default TopContributor;