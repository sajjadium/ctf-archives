import { gql, useQuery } from "@apollo/client";
import { Alert } from "@mui/material";
import { useParams } from "react-router-dom";

export function ExportDetailsPage() {
  const { id } = useParams();

  const { loading, error, data } = useQuery(
    gql`
      query ExportDetailsQuery($id: Int!) {
        export(id: $id) {
          id
          storyId
          dimensions
          progress
          ready
          imageURL
        }
      }
    `,
    {
      variables: { id },
    },
  );

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Export Details</h2>
      {error && <Alert severity="error">Error: {error.message}</Alert>}
      {data && (
        <div>
          <p>Story ID: {data.export.storyId}</p>
          <p>Dimensions: {data.export.dimensions}</p>
          <p>Progress: {data.export.progress}</p>
          <p>Ready: {data.export.ready ? "Yes" : "No"}</p>
          {data.export.imageURL && (
            <img
              src={"/api" + data.export.imageURL}
              alt="Export"
              style={{ maxWidth: "100%" }}
            />
          )}
        </div>
      )}
    </div>
  );
}
