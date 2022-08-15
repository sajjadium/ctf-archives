import * as React from "react";
import {
  Box,
  Heading,
  Container,
  Text,
  Button,
  Stack,
  useColorModeValue,
} from "@chakra-ui/react";
import { Link } from "react-router-dom";

export default function Index() {
  return (
    <>
      <Container maxW="3xl">
        <Stack
          as={Box}
          textAlign="center"
          spacing={{ base: 8, md: 14 }}
          py={{ base: 20, md: 36 }}
        >
          <Heading
            fontWeight={600}
            fontSize={{ base: "2xl", sm: "4xl", md: "6xl" }}
            lineHeight="110%"
          >
            <Text as="span" color="green.400">
              modernblog
            </Text>
          </Heading>
          <Text color={useColorModeValue("dark.500", "light.500")}>
            a simple modern blogging platform. written with the hottest
            front-end libraries.
          </Text>
          <Stack
            direction="column"
            spacing={3}
            align="center"
            alignSelf="center"
            position="relative"
          >
            <Button
              colorScheme="green"
              bg="green.400"
              rounded="full"
              px={6}
              _hover={{
                bg: "green.500",
              }}
              as={Link}
              to="/register"
            >
              Register
            </Button>
            <Button variant="link" colorScheme="blue" as={Link} to="/login">
              Log In
            </Button>
          </Stack>
        </Stack>
      </Container>
    </>
  );
}
