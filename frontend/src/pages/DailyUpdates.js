import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Heading,
  Input,
  Select,
  SimpleGrid,
  Stack,
  Text,
  VStack,
  useToast,
  Spinner,
  Center,
} from "@chakra-ui/react";

import {
  getUpdates,
  addUpdate,
  deleteUpdate,
  getTeamMembers,
  getProjects,
} from "../api/api";

function DailyUpdates() {
  const toast = useToast();

  const [updates, setUpdates] = useState([]);
  const [members, setMembers] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState({
    member_id: "",
    project_id: "",
    update_date: "",
    task_completed: "",
    blockers: "",
    hours_worked: "",
    status: "In Progress",
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      const [updatesRes, membersRes, projectsRes] = await Promise.all([
        getUpdates(),
        getTeamMembers(),
        getProjects(),
      ]);

      setUpdates(updatesRes.data);
      setMembers(membersRes.data);
      setProjects(projectsRes.data);
    } catch (error) {
      console.error(error);

      toast({
        title: "Failed to load data",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const clearForm = () => {
    setForm({
      member_id: "",
      project_id: "",
      update_date: "",
      task_completed: "",
      blockers: "",
      hours_worked: "",
      status: "In Progress",
    });
  };

  const handleSubmit = async () => {
    if (
      !form.member_id ||
      !form.project_id ||
      !form.update_date ||
      !form.task_completed ||
      !form.hours_worked
    ) {
      toast({
        title: "Please fill all required fields",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    try {
      await addUpdate({
        member_id: Number(form.member_id),
        project_id: Number(form.project_id),
        update_date: form.update_date,
        task_completed: form.task_completed,
        blockers: form.blockers,
        hours_worked: Number(form.hours_worked),
        status: form.status,
      });

      toast({
        title: "Daily update added",
        status: "success",
        duration: 3000,
        isClosable: true,
      });

      clearForm();
      loadData();
    } catch (error) {
      console.error(error);

      toast({
        title: "Failed to add update",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteUpdate(id);

      toast({
        title: "Update deleted",
        status: "success",
        duration: 3000,
        isClosable: true,
      });

      loadData();
    } catch (error) {
      console.error(error);

      toast({
        title: "Delete failed",
        status: "error",
      });
    }
  };

  const getMemberName = (id) => {
    const member = members.find((m) => m.id === id);
    return member ? member.full_name : `Member ${id}`;
  };

  const getProjectName = (id) => {
    const project = projects.find((p) => p.id === id);
    return project ? project.project_name : `Project ${id}`;
  };

  if (loading) {
    return (
      <Center h="70vh">
        <Spinner size="xl" />
      </Center>
    );
  }
    return (
    <Container maxW="container.xl" py={8}>
      <Heading mb={6}>Daily Updates</Heading>

      <Box
        p={6}
        borderWidth="1px"
        borderRadius="lg"
        mb={8}
        boxShadow="md"
      >
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={5}>
          <FormControl isRequired>
            <FormLabel>Team Member</FormLabel>
            <Select
              placeholder="Select Team Member"
              name="member_id"
              value={form.member_id}
              onChange={handleChange}
            >
              {members.map((member) => (
                <option key={member.id} value={member.id}>
                  {member.full_name}
                </option>
              ))}
            </Select>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Project</FormLabel>
            <Select
              placeholder="Select Project"
              name="project_id"
              value={form.project_id}
              onChange={handleChange}
            >
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.project_name}
                </option>
              ))}
            </Select>
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Date</FormLabel>
            <Input
              type="date"
              name="update_date"
              value={form.update_date}
              onChange={handleChange}
            />
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Hours Worked</FormLabel>
            <Input
              type="number"
              name="hours_worked"
              value={form.hours_worked}
              onChange={handleChange}
            />
          </FormControl>

          <FormControl>
            <FormLabel>Task Completed</FormLabel>
            <Input
              name="task_completed"
              value={form.task_completed}
              onChange={handleChange}
              placeholder="Completed task..."
            />
          </FormControl>

          <FormControl>
            <FormLabel>Blockers</FormLabel>
            <Input
              name="blockers"
              value={form.blockers}
              onChange={handleChange}
              placeholder="Any blockers?"
            />
          </FormControl>

          <FormControl>
            <FormLabel>Status</FormLabel>
            <Select
              name="status"
              value={form.status}
              onChange={handleChange}
            >
              <option value="Completed">Completed</option>
              <option value="In Progress">In Progress</option>
              <option value="Blocked">Blocked</option>
            </Select>
          </FormControl>
        </SimpleGrid>

        <Button
          mt={6}
          colorScheme="blue"
          onClick={handleSubmit}
        >
          Add Update
        </Button>
      </Box>

      <Heading size="md" mb={5}>
        Recent Updates
      </Heading>

      <VStack spacing={4} align="stretch">
        {updates.length === 0 ? (
          <Text>No updates found.</Text>
        ) : (
          updates.map((update) => (
            <Box
              key={update.id}
              borderWidth="1px"
              borderRadius="lg"
              p={5}
              boxShadow="sm"
            >
              <Stack spacing={2}>
                <Text>
                  <strong>Member:</strong>{" "}
                  {getMemberName(update.member_id)}
                </Text>

                <Text>
                  <strong>Project:</strong>{" "}
                  {getProjectName(update.project_id)}
                </Text>

                <Text>
                  <strong>Date:</strong> {update.update_date}
                </Text>

                <Text>
                  <strong>Task:</strong> {update.task_completed}
                </Text>

                <Text>
                  <strong>Blockers:</strong>{" "}
                  {update.blockers || "None"}
                </Text>

                <Text>
                  <strong>Hours Worked:</strong>{" "}
                  {update.hours_worked}
                </Text>

                <Text>
                  <strong>Status:</strong> {update.status}
                </Text>

                <Button
                  colorScheme="red"
                  size="sm"
                  w="120px"
                  onClick={() => handleDelete(update.id)}
                >
                  Delete
                </Button>
              </Stack>
            </Box>
          ))
        )}
      </VStack>
    </Container>
  );
}

export default DailyUpdates;