import styled from "@emotion/styled";
import { CircularProgress } from "@mui/material";

const Layout = styled.div`
  width: 500px;
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 35px;
`;

export function FullPageLoading() {
  return (
    <Layout>
      <CircularProgress />
      <p>Loading...</p>
    </Layout>
  );
}
