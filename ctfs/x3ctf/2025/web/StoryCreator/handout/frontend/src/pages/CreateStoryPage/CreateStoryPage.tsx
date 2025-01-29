import { gql, useMutation, useQuery } from "@apollo/client";
import styled from "@emotion/styled";
import {
  Alert,
  Button,
  CircularProgress,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from "@mui/material";
import { useSnackbar } from "notistack";
import { useNavigate } from "react-router-dom";
import { FullPageLoading } from "../../components/FullPageLoading";

const Layout = styled.div`
  display: flex;
  flex-direction: column;
  gap: 25px;
`;

export function CreateStoryPage() {
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();

  const {
    loading: queryLoading,
    error: queryError,
    data: queryData,
  } = useQuery(gql`
    query CreateStory {
      images {
        id
        url
      }
    }
  `);

  const [createStory, { loading: mutationLoading, error: mutationError }] =
    useMutation(gql`
      mutation CreateStoryMutation($story: StoryInput!) {
        createStory(story: $story) {
          id
          text
          action
          image {
            id
            url
          }
        }
      }
    `);

  if (queryLoading) {
    return <FullPageLoading />;
  }

  const error = queryError || mutationError;
  const data = queryData;

  return (
    <>
      <h2>Create Story</h2>
      {error && <Alert severity="error">Error: {error.message}</Alert>}
      {data && (
        <form
          onSubmit={async (event) => {
            event.preventDefault();
            const formEl = event.target as HTMLFormElement;
            const formData = new FormData(formEl);

            const image = formData.get("image");
            const text = formData.get("text");
            const action = formData.get("action");
            const result = await createStory({
              variables: {
                story: {
                  image: parseInt(image as string),
                  text: text as string,
                  action: action as string,
                },
              },
            });
            const createdStory = result.data.createStory;
            console.log("createStory", { image, text, action, createdStory });
            enqueueSnackbar("Story created", { variant: "success" });
            navigate(`/stories/${createdStory.id}`);
          }}
        >
          <Layout>
            <FormControl fullWidth={true}>
              <InputLabel htmlFor="image" id="image-label">
                Image
              </InputLabel>
              <Select
                id="image"
                name="image"
                labelId="image-label"
                required={true}
              >
                {data.images.map((image: { id: number; url: string }) => (
                  <MenuItem key={image.id} value={image.id}>
                    {image.url}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl fullWidth={true}>
              <InputLabel htmlFor="text" id="text-label">
                Text
              </InputLabel>
              <TextField
                id="text"
                name="text"
                variant="outlined"
                fullWidth={true}
                multiline={true}
                required={true}
                inputProps={{
                  minLength: 1,
                  maxLength: 100,
                }}
              />
            </FormControl>
            <FormControl fullWidth={true}>
              <InputLabel htmlFor="action" id="action-label">
                Action
              </InputLabel>
              <TextField
                id="action"
                name="action"
                variant="outlined"
                fullWidth={true}
                multiline={true}
                required={true}
                inputProps={{
                  minLength: 1,
                  maxLength: 50,
                }}
              />
            </FormControl>
            <Button type="submit" disabled={mutationLoading}>
              {mutationLoading && <CircularProgress />}
              Create
            </Button>
          </Layout>
        </form>
      )}
    </>
  );
}
