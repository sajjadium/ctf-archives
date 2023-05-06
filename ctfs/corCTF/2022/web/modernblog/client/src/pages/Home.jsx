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
  Textarea,
  Alert,
  AlertIcon,
  AlertTitle,
} from "@chakra-ui/react";
import { Link, useNavigate } from "react-router-dom";

export default function Index() {
  const [posts, setPosts] = React.useState([]);

  const [title, setTitle] = React.useState("");
  const [body, setBody] = React.useState("");
  const [error, setError] = React.useState(null);

  const navigate = useNavigate();

  const create = (e) => {
    e && e.preventDefault();
    if (!title || !body) {
      return setError("Missing title or body.");
    }

    fetch("/api/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, body }),
    })
      .then((r) => r.json())
      .then((resp) => {
        if (!resp.success) {
          return setError(resp.error);
        }
        fetchPosts();
        setTitle("");
        setBody("");
      });
  };

  const fetchPosts = () => {
    fetch("/api/posts", { method: "POST" })
      .then((r) => r.json())
      .then((resp) => {
        if (!resp.success) {
          return navigate("/");
        }
        setPosts(resp.data);
      });
  };

  React.useEffect(fetchPosts, [navigate]);

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

          <Text
            color={useColorModeValue("dark.500", "light.500")}
            fontSize={{ base: "xl", sm: "2xl", md: "3xl" }}
          >
            home
          </Text>

          <Stack
            spacing={4}
            w="full"
            maxW="md"
            bg={useColorModeValue("gray.50", "gray.700")}
            rounded="xl"
            boxShadow="2xl"
            p={6}
            my={12}
          >
            <Heading lineHeight={1.1} fontSize={{ base: "2xl", md: "3xl" }}>
              Your Posts
            </Heading>
            <Stack alignItems="start">
              <ul>
                {posts.map((post, i) => (
                  <Box key={i} ml={4}>
                    <li style={{ textAlign: "left" }}>
                      <Button
                        variant="link"
                        as={Link}
                        to={`/post/${post.id}`}
                        justifyContent="start"
                      >
                        <Text fontSize={{ base: "md", md: "lg" }}>
                          {post.title}
                        </Text>
                      </Button>
                    </li>
                  </Box>
                ))}
              </ul>
            </Stack>
          </Stack>

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
            onSubmit={create}
          >
            <Heading lineHeight={1.1} fontSize={{ base: "2xl", md: "3xl" }}>
              Create Post
            </Heading>
            {error && (
              <Alert status="error" variant="solid">
                <AlertIcon />
                <AlertTitle>{error}</AlertTitle>
              </Alert>
            )}
            <FormControl>
              <Input
                placeholder="title"
                _placeholder={{ color: "gray.500" }}
                type="text"
                onChange={(e) => setTitle(e.target.value)}
                value={title}
              />
            </FormControl>
            <FormControl>
              <Textarea
                placeholder="body"
                _placeholder={{ color: "gray.500" }}
                onChange={(e) => setBody(e.target.value)}
                value={body}
              />
            </FormControl>
            <Stack spacing={6}>
              <Button
                bg="blue.400"
                color="white"
                _hover={{
                  bg: "blue.500",
                }}
                type="submit"
                onClick={create}
              >
                Create
              </Button>
            </Stack>
          </Stack>
        </Stack>
      </Container>
    </>
  );
}
