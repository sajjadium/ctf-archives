import { gql, useQuery } from "@apollo/client";
import { Alert } from "@mui/material";

export function ExportListPage() {
  const { loading, error, data } = useQuery(gql`
    query ExportlistQuery {
      exports {
        id
        progress
        ready
      }
    }
  `);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Export Details</h2>
      {error && <Alert severity="error">Error: {error.message}</Alert>}
      {data && (
        <div>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Progress</th>
                <th>Ready</th>
              </tr>
            </thead>
            <tbody>
              {data.exports.map(
                (exportItem: {
                  id: string;
                  progress: string;
                  ready: boolean;
                }) => (
                  <tr key={exportItem.id}>
                    <td>
                      <a href={"/export/" + exportItem.id}>{exportItem.id}</a>
                    </td>
                    <td>{exportItem.progress}</td>
                    <td>{exportItem.ready ? "Yes" : "No"}</td>
                  </tr>
                ),
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
