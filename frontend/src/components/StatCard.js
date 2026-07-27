import {
  Box,
  Flex,
  Text,
  Stat,
  StatNumber,
  Icon,
} from "@chakra-ui/react";

import {
  FiArrowUpRight,
} from "react-icons/fi";

function StatCard({
  title,
  value,
  color,
  icon,
}) {
  return (
    <Box
      bg="white"
      p={6}
      borderRadius="2xl"
      boxShadow="sm"
      transition=".3s"
      border="1px solid"
      borderColor="gray.100"
      _hover={{
        transform: "translateY(-6px)",
        boxShadow: "2xl",
      }}
    >
      <Flex
        justify="space-between"
        align="center"
        mb={5}
      >
        <Box
          bg={color}
          color="white"
          p={3}
          borderRadius="xl"
        >
          <Icon
            as={icon}
            boxSize={5}
          />
        </Box>

        <Text
          color="gray.500"
          fontWeight="600"
          fontSize="sm"
        >
          LIVE
        </Text>
      </Flex>

      <Stat>
        <Text
          color="gray.500"
          mb={2}
        >
          {title}
        </Text>

        <StatNumber
          fontSize="4xl"
          color="gray.800"
        >
          {value}
        </StatNumber>
      </Stat>
    </Box>
  );
}

export default StatCard;