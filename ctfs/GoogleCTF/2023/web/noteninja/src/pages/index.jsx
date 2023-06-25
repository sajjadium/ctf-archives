import FetchNotes from "@/sources/components/FetchNotes";
import Protector from "@/sources/components/Layout/Protector";

export default function Home() {
  return (
    <Protector>
      <div className="p-20 flex flex-col gap-5">
        <div className="text-4xl font-semibold">All Notes:</div>
        <FetchNotes />
      </div>
    </Protector>
  );
}
