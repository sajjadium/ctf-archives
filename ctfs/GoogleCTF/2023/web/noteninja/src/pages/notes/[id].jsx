import Protector from "@/sources/components/Layout/Protector";
import ViewNote from "@/sources/components/ViewNote";
import { useRouter } from "next/router";
import React from "react";

const Page = () => {
  const router = useRouter();
  const { id } = router.query;

  return (
    <Protector>
      <ViewNote id={id} />
    </Protector>
  );
};

export default Page;
