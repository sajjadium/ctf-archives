import type { GetServerSideProps, NextPage } from "next";
import type { User } from "@prisma/client";
import { prisma } from "../globals/prisma";
import { useState } from "react";
import { useRouter } from "next/router";

type Props = {
  users: (User &
    (
      | {
          flag: string;
          isAdmin: true;
        }
      | {
          flag?: never;
          isAdmin: false;
        }
    ))[];
};

const Home: NextPage<Props> = ({ users }) => {
  const [username, setUsername] = useState("");

  const router = useRouter();

  const create = async () => {
    await fetch("/api/auth", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({
        username,
      }),
    });
    await router.replace(router.asPath);
  };

  return (
    <div>
      <div>Create user:</div>
      <input
        value={username}
        onChange={(event) => setUsername(event.target.value)}
      />
      <button onClick={create}>Create</button>
      <div>Users:</div>
      {users.map((user) => (
        <div key={user.id}>
          <div>Username: {user.username}</div>
          <div>Is admin? {user.isAdmin ? "yes" : "no"}</div>
          {user.isAdmin && <div>{user.flag}</div>}
        </div>
      ))}
    </div>
  );
};

export default Home;

export const getServerSideProps: GetServerSideProps<Props> = async (
  context
) => {
  const users = (await prisma.user.findMany()) as Props["users"];

  for (const user of users) {
    if (user.isAdmin) {
      user.flag = process.env.FLAG!;
    }
  }

  return {
    props: {
      users,
    },
  };
};
