import * as React from "react";
import {
  Box,
  Heading,
  Container,
  Text,
  Button,
  Stack,
  useColorModeValue,
  FormControl,
  Input,
  Alert,
  AlertTitle,
  AlertIcon,
} from "@chakra-ui/react";
import { useNavigate, Link } from "react-router-dom";

export default function Register() {
  const [user, setUser] = React.useState("");
  const [pass, setPass] = React.useState("");
  const [error, setError] = React.useState(null);

  const navigate = useNavigate();

  const register = async (e) => {
    e && e.preventDefault();
    if (!user || !pass) {
      return setError("Missing username or password.");
    }

    fetch("/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user, pass }),
    })
      .then((r) => r.json())
      .then((resp) => {
        if (!resp.success) {
          return setError(resp.error);
        }
        navigate("/home");
      });
  };

  return (
    <>
      <Container maxW="3xl">
        <Stack
          as={Box}
          textAlign="center"
          spacing={{ base: 8, md: 14 }}
          py={{ base: 20, md: 36 }}
          alignItems="center"
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

          <Stack
            spacing={4}
            w="full"
            maxW="md"
            bg={useColorModeValue("gray.50", "gray.700")}
            rounded="xl"
            boxShadow="2xl"
            p={6}
            my={12}
            as="form"
            onSubmit={register}
          >
            <Heading lineHeight={1.1} fontSize={{ base: "2xl", md: "3xl" }}>
              Register
            </Heading>
            {error && (
              <Alert status="error" variant="solid">
                <AlertIcon />
                <AlertTitle>{error}</AlertTitle>
              </Alert>
            )}
            <FormControl>
              <Input
                placeholder="username"
                name="user"
                _placeholder={{ color: "gray.500" }}
                type="text"
                onChange={(e) => setUser(e.target.value)}
                value={user}
              />
            </FormControl>
            <FormControl>
              <Input
                placeholder="password"
                name="pass"
                _placeholder={{ color: "gray.500" }}
                type="password"
                onChange={(e) => setPass(e.target.value)}
                value={pass}
              />
            </FormControl>
            <Stack spacing={6}>
              <Button
                bg="blue.400"
                color="white"
                _hover={{
                  bg: "blue.500",
                }}
                onClick={register}
                type="submit"
              >
                Register
              </Button>
            </Stack>
            <Button variant="link" as={Link} to="/">
              Back
            </Button>
          </Stack>
        </Stack>
      </Container>
    </>
  );
}
