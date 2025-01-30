import { Alert } from "@mui/material";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { FullPageLoading } from "../../components/FullPageLoading";
import { RenderStory } from "../../components/story";

interface Response {
  story: {
    id: number;
    text: string;
    action: string;
    image: {
      url: string;
    };
  };
}

export function Render() {
  const { id } = useParams();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<Response | null>(null);
  const [error, setError] = useState<Error | null>(null);
  useEffect(() => {
    const ac = new AbortController();
    setLoading(true);
    fetch("/api/graphql", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: "",
        variables: { id },
        extensions: {
          persistedQuery: {
            version: 1,
            sha256Hash:
              "d15293ae32151343d3a893f1c0417f664d573ae322394c44ce30b002ad6e22c9",
          },
        },
      }),
      signal: ac.signal,
    })
      .then((data) => data.json())
      .then((data) => {
        if (data.errors && data.errors.length > 0) {
          if (data.errors[0].message === "PersistedQueryNotFound") {
            return fetch("/api/graphql", {
              method: "POST",
              credentials: "include",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                query: `query ViewStoryPage($id: Int!) {
                    story(id: $id) {
                      id
                      text
                      action
                      image {
                        url
                      }
                    }
                  }`,
                variables: { id },
                extensions: {
                  persistedQuery: {
                    version: 1,
                    sha256Hash:
                      "d15293ae32151343d3a893f1c0417f664d573ae322394c44ce30b002ad6e22c9",
                  },
                },
              }),
              signal: ac.signal,
            }).then((data) => data.json());
          }
        }
        return data;
      })
      .then((data) => {
        setData(data.data);
        setLoading(false);
        setError(null);
      });

    return () => {
      ac.abort("useEffect cancellation");
      setLoading(false);
    };
  }, [id]);

  if (loading) {
    return <FullPageLoading />;
  }

  return (
    <>
      {error && <Alert severity="error">Error: {error.message}</Alert>}
      {data && (
        <RenderStory
          story={data.story}
          fields={data as unknown as Record<string, string>}
        />
      )}
    </>
  );
}
