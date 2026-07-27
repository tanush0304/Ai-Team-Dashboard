import {
  Box,
  Heading,
  Text,
  SimpleGrid,
} from "@chakra-ui/react";

import {
  Doughnut,
  Bar,
} from "react-chartjs-2";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from "chart.js";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
);

function DashboardCharts({
  updates,
  members,
}) {

  const completed = updates.filter(
    u => u.status === "Completed"
  ).length;

  const progress = updates.filter(
    u => u.status === "In Progress"
  ).length;

  const blocked = updates.filter(
    u => u.status === "Blocked"
  ).length;

  const memberHours = {};

  updates.forEach(update => {
    const member = members.find(
      m => m.id === update.member_id
    );

    const name = member
      ? member.full_name
      : "Unknown";

    memberHours[name] =
      (memberHours[name] || 0) +
      Number(update.hours_worked);
  });

  const doughnutData = {
    labels: [
      "Completed",
      "In Progress",
      "Blocked",
    ],
    datasets: [
      {
        data: [
          completed,
          progress,
          blocked,
        ],
        backgroundColor: [
          "#22C55E",
          "#FACC15",
          "#EF4444",
        ],
        borderWidth: 0,
      },
    ],
  };

  const doughnutOptions = {
    cutout: "70%",
    plugins: {
      legend: {
        position: "bottom",
      },
    },
  };

  const barData = {
    labels: Object.keys(memberHours),
    datasets: [
      {
        label: "Hours Worked",
        data: Object.values(memberHours),
        backgroundColor: "#4F46E5",
        borderRadius: 8,
        maxBarThickness: 35,
      },
    ],
  };

  const barOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  const cardStyle = {
    bg: "white",
    p: 6,
    borderRadius: "2xl",
    boxShadow: "sm",
    border: "1px solid",
    borderColor: "gray.100",
    transition: ".3s",
    _hover: {
      transform: "translateY(-4px)",
      boxShadow: "xl",
    },
  };

  return (
    <SimpleGrid
      columns={{ base: 1, xl: 2 }}
      spacing={6}
    >

      <Box {...cardStyle}>
        <Heading size="md">
          Project Status
        </Heading>

        <Text
          color="gray.500"
          mb={5}
        >
          Current task distribution
        </Text>

        <Doughnut
          data={doughnutData}
          options={doughnutOptions}
        />
      </Box>

      <Box {...cardStyle}>
        <Heading size="md">
          Team Productivity
        </Heading>

        <Text
          color="gray.500"
          mb={5}
        >
          Total hours worked
        </Text>

        <Bar
          data={barData}
          options={barOptions}
        />
      </Box>

    </SimpleGrid>
  );
}

export default DashboardCharts;