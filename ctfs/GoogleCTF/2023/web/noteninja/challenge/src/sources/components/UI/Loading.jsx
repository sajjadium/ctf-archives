import React from "react";
import { ImSpinner2 } from "react-icons/im";

const Loading = ({ height }) => {
  return (
    <div
      className={`flex items-center justify-center ${
        height ? height : "h-[80vh]"
      }`}
    >
      <ImSpinner2 className="animate-spin text-4xl" />
    </div>
  );
};

export default Loading;
