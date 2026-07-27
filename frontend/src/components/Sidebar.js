import {
  Box,
  VStack,
  Text,
  Flex,
  Icon,
  Badge,
  Divider,
  Spacer,
} from "@chakra-ui/react";

import {
  FiHome,
  FiUsers,
  FiFolder,
  FiClipboard,
  FiCpu,
} from "react-icons/fi";

import { NavLink } from "react-router-dom";

const menu = [
  {
    section: "MAIN",
    items: [
      {
        name: "Dashboard",
        icon: FiHome,
        path: "/",
      },
      {
        name: "Team Members",
        icon: FiUsers,
        path: "/team",
      },
      {
        name: "Projects",
        icon: FiFolder,
        path: "/projects",
      },
      {
        name: "Daily Updates",
        icon: FiClipboard,
        path: "/updates",
      },
    ],
  },
  {
    section: "AI",
    items: [
      {
        name: "AI Assistant",
        icon: FiCpu,
        path: "/ai",
        badge: "NEW",
      },
    ],
  },

];

function Sidebar() {
  return (
    <Box
      position="fixed"
      left="0"
      top="0"
      w="280px"
      h="100vh"
      bg="linear-gradient(180deg,#111827,#1E293B)"
      color="white"
      display="flex"
      flexDirection="column"
      boxShadow="2xl"
    >
      {/* Logo */}

      <Box px={6} py={8}>
        <Text
          fontSize="3xl"
          fontWeight="800"
          color="white"
        >
          ⚡ AI Team
        </Text>

        <Text
          color="gray.400"
          fontSize="sm"
          mt={1}
        >
          Team Management Dashboard
        </Text>
      </Box>

      <Divider borderColor="gray.700" />

      <VStack
        align="stretch"
        spacing={6}
        px={4}
        py={6}
        flex="1"
      >
        {menu.map((group) => (
          <Box key={group.section}>
            <Text
              fontSize="xs"
              color="gray.500"
              mb={3}
              px={3}
              fontWeight="bold"
            >
              {group.section}
            </Text>

            <VStack spacing={2} align="stretch">
              {group.items.map((item) => (
                <NavLink
                  key={item.name}
                  to={item.path}
                  style={{
                    textDecoration: "none",
                  }}
                >
                  {({ isActive }) => (
                    <Flex
                      align="center"
                      px={4}
                      py={3}
                      borderRadius="xl"
                      borderLeft={
                          isActive
                          ? "4px solid #60A5FA"
                          : "4px solid transparent"
                        }
                      bg={
                          isActive
                          ? "whiteAlpha.200"
                          : "transparent"
                        }
                      color={
                        isActive
                          ? "white"
                          : "gray.300"
                      }
                      transition="all .25s"
                      _hover={{
                        bg: "gray.700",
                        transform:
                          "translateX(6px)",
                      }}
                    >
                      <Icon
                        as={item.icon}
                        boxSize={5}
                      />

                      <Text
                        ml={4}
                        flex="1"
                        fontWeight="medium"
                      >
                        {item.name}
                      </Text>

                      {item.badge && (
                        <Badge
                          colorScheme="purple"
                          borderRadius="full"
                        >
                          {item.badge}
                        </Badge>
                      )}
                    </Flex>
                  )}
                </NavLink>
              ))}
            </VStack>
          </Box>
        ))}

        <Spacer />
      </VStack>

      <Divider borderColor="gray.700" />

      {/* User Card */}

      
    </Box>
  );
}

export default Sidebar;