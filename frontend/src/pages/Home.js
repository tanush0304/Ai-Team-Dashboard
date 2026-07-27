import { useEffect, useState } from "react";
import {
  Heading,
  SimpleGrid,
  Spinner,
  Center,
  Box,
  Text,
  VStack,
} from "@chakra-ui/react";

import {
  FiUsers,
  FiFolder,
  FiClipboard,
  FiClock,
} from "react-icons/fi";

import {
  getTeamMembers,
  getProjects,
  getUpdates,
} from "../api/api";

import StatCard from "../components/StatCard";
import DashboardCharts from "../components/DashboardCharts";
import RecentUpdates from "../components/RecentUpdates";
import TopContributor from "../components/TopContributor";

function Home() {
  const [loading, setLoading] = useState(true);

  const [stats, setStats] = useState({
    team: 0,
    projects: 0,
    updates: 0,
    avgHours: 0,
  });

  const [members, setMembers] = useState([]);
  const [projects, setProjects] = useState([]);
  const [allUpdates, setAllUpdates] = useState([]);
  const [recentUpdates, setRecentUpdates] = useState([]);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const [teamRes, projectRes, updateRes] =
        await Promise.all([
          getTeamMembers(),
          getProjects(),
          getUpdates(),
        ]);

      const membersData = teamRes.data;
      const projectsData = projectRes.data;
      const updatesData = updateRes.data;

      setMembers(membersData);
      setProjects(projectsData);
      setAllUpdates(updatesData);

      setRecentUpdates(
        [...updatesData]
          .sort((a, b) => b.id - a.id)
          .slice(0, 5)
      );

      const totalHours = updatesData.reduce(
        (sum, item) =>
          sum + Number(item.hours_worked || 0),
        0
      );

      const avgHours =
        updatesData.length > 0
          ? (totalHours / updatesData.length).toFixed(1)
          : 0;

      setStats({
        team: membersData.length,
        projects: projectsData.length,
        updates: updatesData.length,
        avgHours,
      });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Center h="70vh">
        <Spinner size="xl" color="blue.500" />
      </Center>
    );
  }

  return (
    <VStack spacing={8} align="stretch">

      <Box>
        <Heading size="lg" color="gray.800">
          AI Team Dashboard
        </Heading>

        <Text color="gray.500" mt={1}>
          Monitor your team, projects and AI insights.
        </Text>
      </Box>

      <SimpleGrid
        columns={{ base: 1, md: 2, xl: 4 }}
        spacing={6}
      >
        <StatCard
          title="Team Members"
          value={stats.team}
          color="blue.500"
          icon={FiUsers}
        />

        <StatCard
          title="Projects"
          value={stats.projects}
          color="green.500"
          icon={FiFolder}
        />

        <StatCard
          title="Daily Updates"
          value={stats.updates}
          color="purple.500"
          icon={FiClipboard}
        />

        <StatCard
          title="Average Hours"
          value={stats.avgHours}
          color="orange.400"
          icon={FiClock}
        />
      </SimpleGrid>

      <DashboardCharts
        updates={allUpdates}
        members={members}
      />

      <SimpleGrid
        columns={{ base: 1, xl: 2 }}
        spacing={6}
      >
        <TopContributor
          updates={allUpdates}
          members={members}
        />

        <RecentUpdates
          updates={recentUpdates}
          members={members}
          projects={projects}
        />
      </SimpleGrid>

    </VStack>
  );
}

export default Home;