import {
  Avatar,
  Badge,
  Box,
  Divider,
  Flex,
  Heading,
  HStack,
  Text,
  VStack,
} from "@chakra-ui/react";

function RecentUpdates({
  updates,
  members,
  projects,
}) {

  const memberName = (id) =>
    members.find((m) => m.id === id)
      ?.full_name || "Unknown";

  const projectName = (id) =>
    projects.find((p) => p.id === id)
      ?.project_name || "Unknown";

  const badgeColor = (status) => {
    switch (status) {
      case "Completed":
        return "green";

      case "Blocked":
        return "red";

      default:
        return "yellow";
    }
  };

  return (
    <Box
      bg="white"
      borderRadius="2xl"
      p={6}
      boxShadow="sm"
      border="1px solid"
      borderColor="gray.100"
    >
      <Heading
        size="md"
        mb={6}
      >
        Recent Activity
      </Heading>

      <VStack
        spacing={5}
        align="stretch"
      >
        {updates.map((update) => (

          <Box
            key={update.id}
          >

            <Flex
              justify="space-between"
              align="center"
            >

              <HStack
                spacing={4}
                align="start"
              >

                <Avatar
                  size="sm"
                  name={memberName(
                    update.member_id
                  )}
                  bg="blue.500"
                />

                <Box>

                  <Text
                    fontWeight="bold"
                  >
                    {memberName(
                      update.member_id
                    )}
                  </Text>

                  <Text
                    color="gray.600"
                    fontSize="sm"
                    mt={1}
                  >
                    {update.task_completed}
                  </Text>

                  <Text
                    fontSize="xs"
                    color="gray.500"
                    mt={2}
                  >
                    📁 {projectName(update.project_id)}
                  </Text>

                  <Text
                    fontSize="xs"
                    color="gray.500"
                  >
                    ⏱ {update.hours_worked} hrs
                  </Text>

                  <Text
                    fontSize="xs"
                    color="gray.500"
                  >
                    📅 {update.update_date}
                  </Text>

                  {update.blockers &&
                    update.blockers !== "None" && (

                    <Text
                      mt={2}
                      color="red.500"
                      fontSize="sm"
                    >
                      🚧 {update.blockers}
                    </Text>

                  )}

                </Box>

              </HStack>

              <Badge
                colorScheme={badgeColor(
                  update.status
                )}
                borderRadius="full"
                px={3}
                py={1}
              >
                {update.status}
              </Badge>

            </Flex>

            <Divider mt={5} />

          </Box>

        ))}
      </VStack>

    </Box>
  );
}

export default RecentUpdates;