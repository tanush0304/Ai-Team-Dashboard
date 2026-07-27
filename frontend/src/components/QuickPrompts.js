import {
  Box,
  Heading,
  SimpleGrid,
  Button,
} from "@chakra-ui/react";

const prompts = [
  "How many team members are there?",
  "List all projects",
  "Who worked the most hours?",
  "Show blocked tasks",
  "List completed updates",
  "Summarize today's work",
];

function QuickPrompts({ onSelect }) {
  return (
    <Box mb={6}>
      <Heading
        size="sm"
        mb={4}
        color="gray.600"
      >
        Quick Questions
      </Heading>

      <SimpleGrid
        columns={{
          base: 1,
          md: 2,
          lg: 3,
        }}
        spacing={3}
      >
        {prompts.map((prompt) => (
          <Button
            key={prompt}
            justifyContent="flex-start"
            variant="outline"
            borderRadius="xl"
            colorScheme="blue"
            h="55px"
            whiteSpace="normal"
            onClick={() => onSelect(prompt)}
            _hover={{
              transform: "translateY(-2px)",
              boxShadow: "md",
            }}
          >
            {prompt}
          </Button>
        ))}
      </SimpleGrid>
    </Box>
  );
}

export default QuickPrompts;