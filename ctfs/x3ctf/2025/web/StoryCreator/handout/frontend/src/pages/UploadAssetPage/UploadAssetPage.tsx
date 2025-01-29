import { gql, useMutation } from "@apollo/client";
import styled from "@emotion/styled";
import { Alert, Button, FormControl } from "@mui/material";
import { useSnackbar } from "notistack";
import { useNavigate } from "react-router-dom";

const Layout = styled.div`
  display: flex;
  flex-direction: column;
  gap: 25px;
`;

export function UploadAssetPage() {
  const { enqueueSnackbar } = useSnackbar();
  const navigate = useNavigate();
  const [upload, { loading, error }] = useMutation(gql`
    mutation UploadImage($file: Upload!) {
      uploadImage(file: $file)
    }
  `);
  return (
    <>
      <h2>Upload Asset</h2>
      {error && <Alert severity="error">Error: {error.message}</Alert>}
      <form
        onSubmit={async (event) => {
          event.preventDefault();
          if (loading) {
            return;
          }
          const formEl = event.target as HTMLFormElement;
          if (!checkValidity(formEl)) {
            return;
          }
          const fileEl = formEl.querySelector("#file") as HTMLInputElement;
          if (!fileEl.files) {
            return;
          }
          const file = fileEl.files[0];
          await upload({ variables: { file } });
          enqueueSnackbar("Upload completed!", { variant: "success" });
          navigate("/new");
        }}
      >
        <Layout>
          <FormControl fullWidth={true}>
            <input type="file" id="file" accept="image/png" required />
          </FormControl>
          <Button type="submit" disabled={loading}>
            Upload
          </Button>
        </Layout>
      </form>
    </>
  );
}

function checkValidity(el: HTMLFormElement) {
  const fileEl = el.querySelector("#file") as HTMLInputElement;
  if (!fileEl.files) {
    fileEl.setCustomValidity("Time to select a file");
    return false;
  }
  if (fileEl.files.length !== 1) {
    fileEl.setCustomValidity("Exactly 1 file please");
    return false;
  }

  if (fileEl.files[0].size > 100 * 1024) {
    fileEl.setCustomValidity("File is more than 100 kb");
    return false;
  }
  return true;
}
