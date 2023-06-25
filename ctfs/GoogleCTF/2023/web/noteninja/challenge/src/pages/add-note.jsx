import AddNotes from "@/sources/components/AddNotes";
import Protector from "@/sources/components/Layout/Protector";
import React from "react";

const Page = () => {
  return (
    <Protector>
      <AddNotes />
    </Protector>
  );
};

export default Page;
