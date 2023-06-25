import EditNotes from "@/sources/components/EditNotes";
import Protector from "@/sources/components/Layout/Protector";
import { useRouter } from "next/router";
import React from "react";

const Page = () => {
  const router = useRouter();
  const { id } = router.query;

  return (
    <Protector>
      <EditNotes id={id} />
    </Protector>
  );
};

export default Page;
