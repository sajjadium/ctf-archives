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
import { Link, useParams, useNavigate } from "react-router-dom";

export default function Index() {
  const [title, setTitle] = React.useState("");
  const [body, setBody] = React.useState("");

  const navigate = useNavigate();
  const { id } = useParams();

  React.useEffect(() => {
    fetch("/api/post/" + encodeURIComponent(id))
      .then((r) => r.json())
      .then((resp) => {
        if (!resp.success) {
          return navigate("/home");
        }
        setTitle(resp.data.title);
        setBody(resp.data.body);
      });
  }, [id, navigate]);

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
          >
            <Heading lineHeight={1.1} fontSize={{ base: "2xl", md: "3xl" }}>
              {title}
            </Heading>

            {/* CSP is on, so this should be fine, right? */}
            {/* Clueless */}
            <div dangerouslySetInnerHTML={{ __html: body }}></div>
          </Stack>

          <Button variant="link" as={Link} to="/home">
            Back
          </Button>
        </Stack>
      </Container>
    </>
  );
}
