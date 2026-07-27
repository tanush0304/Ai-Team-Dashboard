import { Box, Flex } from "@chakra-ui/react";
import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

function Layout() {
  return (
    <Flex bg="#F5F7FB" minH="100vh">
      <Sidebar />

      <Box
        flex="1"
        ml="280px"
        display="flex"
        flexDirection="column"
      >
        <Topbar />

        <Box
          p={8}
          flex="1"
          bg="#F5F7FB"
        >
          <Outlet />
        </Box>
      </Box>
    </Flex>
  );
}

export default Layout;