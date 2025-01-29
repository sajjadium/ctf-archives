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
} from "@mui/material";
import { useSnackbar } from "notistack";
import { useNavigate } from "react-router-dom";
import { FullPageLoading } from "../../components/FullPageLoading";

const Layout = styled.div`
  display: flex;
  flex-direction: column;
  gap: 25px;
`;

const DIMENSIONS = [
  { value: "FLIPPER_ZERO", label: "Flipper Zero" },
  { value: "SAMSUNG_GALAXY_FOLD", label: "Samsung Galaxy Fold" },
  { value: "IPHONE_14", label: "iPhone 14" },
  { value: "IPHONE_14_MAX", label: "iPhone 14 Max" },
  { value: "SQUARE_400x400", label: "Square (400 x 400)" },
];

export function ExportStoryPage() {
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const {
    loading: queryLoading,
    error: queryError,
    data: queryData,
  } = useQuery(gql`
    query ExportStoryQuery {
      stories {
        id
        text
      }
    }
  `);
  const [mutate, { loading: mutationLoading, error: mutationError }] =
    useMutation(gql`
      mutation CreateExport($export: StoryExportInput!) {
        createStoryExport(export: $export) {
          id
        }
      }
    `);

  if (queryLoading) {
    return <FullPageLoading />;
  }

  return (
    <>
      <h2>Export Story</h2>
      {queryError && <Alert severity="error">{queryError.message}</Alert>}
      {mutationError && <Alert severity="error">{mutationError.message}</Alert>}
      {queryData && (
        <form
          onSubmit={async (event) => {
            event.preventDefault();

            const formEl = event.target as HTMLFormElement;
            const formData = new FormData(formEl);

            const dimensions = formData.get("dimensions");
            const storyId = formData.get("story");
            const result = await mutate({
              variables: {
                export: {
                  storyId,
                  dimensions,
                },
              },
            });
            const createdExport = result.data.createStoryExport;
            console.log("createStoryExport", { storyId, dimensions });
            enqueueSnackbar("Export has been scheduled!", {
              variant: "success",
            });
            navigate(`/export/${createdExport.id}`);
          }}
        >
          <Layout>
            <FormControl fullWidth={true}>
              <InputLabel htmlFor="story" id="story-label">
                Story
              </InputLabel>
              <Select
                id="story"
                name="story"
                labelId="story-label"
                required={true}
              >
                {queryData.stories.map(
                  (story: { id: number; text: string }) => (
                    <MenuItem key={story.id} value={story.id}>
                      {story.text.slice(0, 20)} (ID {story.id})
                    </MenuItem>
                  ),
                )}
              </Select>
            </FormControl>
            <FormControl fullWidth={true}>
              <InputLabel htmlFor="dimensions" id="dimensions-label">
                Dimensions
              </InputLabel>
              <Select
                id="dimensions"
                name="dimensions"
                labelId="dimensions-label"
                required={true}
              >
                {DIMENSIONS.map((dim) => (
                  <MenuItem key={dim.value} value={dim.value}>
                    {dim.label}
                  </MenuItem>
                ))}
              </Select>
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
