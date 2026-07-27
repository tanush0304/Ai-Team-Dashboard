import { useEffect, useState } from "react";
import {
  Box,
  Button,
  Heading,
  Input,
  VStack,
  HStack,
  Text,
} from "@chakra-ui/react";

import {
  getTeamMembers,
  addTeamMember,
  deleteTeamMember,
} from "../api/api";

function TeamMembers() {
  const [members, setMembers] = useState([]);
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [email, setEmail] = useState("");
  const [department, setDepartment] = useState("");
  
  const fetchMembers = async () => {
    try {
      const res = await getTeamMembers();
      setMembers(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchMembers();
  }, []);

  const handleAdd = async () => {
    if (!name || !role) return;

    try {
      await addTeamMember({
        full_name: name,
        email: email,
        role: role,
        department: department,
    });

      setName("");
      setRole("");
      setEmail("");
      setDepartment("");

      fetchMembers();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteTeamMember(id);
      fetchMembers();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Box>
      <Heading mb={6}>Team Members</Heading>

      <HStack mb={5}>
        <Input
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <Input
          placeholder="Role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />
        <Input
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Input
          placeholder="Department"
          value={department}
          onChange={(e) => setDepartment(e.target.value)}
        />

        <Button colorScheme="blue" onClick={handleAdd}>
          Add
        </Button>
      </HStack>

      <VStack spacing={4} align="stretch">
        {members.map((member) => (
          <HStack
            key={member.id}
            bg="white"
            p={4}
            borderRadius="lg"
            justify="space-between"
            boxShadow="sm"
          >
            <Box>
              <Text fontWeight="bold">{member.full_name}</Text>
              <Text>{member.role}</Text>
              <Text>{member.department}</Text>
              <Text fontSize="sm" color="gray.500">
                {member.email}
              </Text>
            </Box>
            <Button
              colorScheme="red"
              size="sm"
              onClick={() => handleDelete(member.id)}
            >
              Delete
            </Button>
          </HStack>
        ))}
      </VStack>
    </Box>
  );
}

export default TeamMembers;