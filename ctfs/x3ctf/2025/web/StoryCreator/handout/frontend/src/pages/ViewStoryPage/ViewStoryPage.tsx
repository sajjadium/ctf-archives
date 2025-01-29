import { gql, useQuery } from "@apollo/client";
import { Alert } from "@mui/material";
import { useParams } from "react-router-dom";
import { FullPageLoading } from "../../components/FullPageLoading";
import { RenderStory } from "../../components/story";

export function ViewStoryPage() {
  const { id } = useParams();
  const { data, loading, error } = useQuery(
    gql`
      query ViewStoryPage($id: Int!) {
        foo
        story(id: $id) {
          id
          text
          action
          image {
            url
          }
        }
      }
    `,
    { variables: { id } },
  );

  if (loading) {
    return <FullPageLoading />;
  }

  return (
    <>
      <h2>View Story</h2>
      {error && <Alert severity="error">Error: {error.message}</Alert>}
      {data && <RenderStory story={data.story} fields={data} />}
    </>
  );
}
