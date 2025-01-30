import { gql, useQuery } from "@apollo/client";
import { Alert } from "@mui/material";
import { NavLink } from "react-router-dom";
import { FullPageLoading } from "../../components/FullPageLoading";

export function ListStoriesPage() {
  const { loading, error, data } = useQuery(gql`
    query ListStories {
      stories {
        id
        text
      }
    }
  `);

  if (loading) {
    return <FullPageLoading />;
  }

  return (
    <>
      <h1>My Stories</h1>
      {error && <Alert severity="error">Error: {error.message}</Alert>}
      <ul>
        {data.stories.map((story: { id: number; text: string }) => (
          <li key={story.id}>
            <NavLink to={`/stories/${story.id}`}>{story.text}</NavLink>
          </li>
        ))}
      </ul>
    </>
  );
}
