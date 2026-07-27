import { useEffect, useState } from "react";
import {
  Box,
  Button,
  Heading,
  Input,
  VStack,
  HStack,
  Text,
  Select,
} from "@chakra-ui/react";

import {
  getProjects,
  addProject,
  deleteProject,
} from "../api/api";

function Projects() {
  const [projects, setProjects] = useState([]);

  const [projectName, setProjectName] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("Planning");

  const fetchProjects = async () => {
    try {
      const res = await getProjects();
      setProjects(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleAdd = async () => {
    if (!projectName || !description) return;

    try {
      await addProject({
        project_name: projectName,
        description: description,
        status: status,
      });

      setProjectName("");
      setDescription("");
      setStatus("Planning");

      fetchProjects();
    } catch (err) {
      console.error(err.response?.data || err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteProject(id);
      fetchProjects();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Box>
      <Heading mb={6}>Projects</Heading>

      <VStack spacing={4} align="stretch" mb={8}>
        <Input
          placeholder="Project Name"
          value={projectName}
          onChange={(e) => setProjectName(e.target.value)}
        />

        <Input
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <Select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        >
          <option value="Planning">Planning</option>
          <option value="In Progress">In Progress</option>
          <option value="Completed">Completed</option>
        </Select>

        <Button colorScheme="blue" onClick={handleAdd}>
          Add Project
        </Button>
      </VStack>

      <VStack spacing={4} align="stretch">
        {projects.length === 0 ? (
          <Text>No projects found.</Text>
        ) : (
          projects.map((project) => (
            <HStack
              key={project.id}
              bg="white"
              p={5}
              borderRadius="lg"
              justify="space-between"
              boxShadow="sm"
            >
              <Box>
                <Text fontWeight="bold" fontSize="lg">
                  {project.project_name}
                </Text>

                <Text>{project.description}</Text>

                <Text color="blue.500" fontWeight="600">
                  {project.status}
                </Text>
              </Box>

              <Button
                colorScheme="red"
                onClick={() => handleDelete(project.id)}
              >
                Delete
              </Button>
            </HStack>
          ))
        )}
      </VStack>
    </Box>
  );
}

export default Projects;