import { CustomFlowbiteTheme, Flowbite, TextInput } from "flowbite-react";
import { useMemo, useRef, useState } from "react";

const customTheme: CustomFlowbiteTheme = {
  textInput: {
    field: {
      input: {
        colors: {
          gray: "bg-stone-50 border-stone-300 focus:outline-stone-400 focus:outline-2 placeholder-stone-500 placeholder:text-md",
          failure:
            "border-red-500 bg-red-50 text-red-900 focus:outline-red-500 focus:outline-2",
          success:
            "border-green-500 bg-green-50 text-green-900 focus:outline-green-500 focus:outline-2",
        },
      },
    },
  },
};

function debounce(func: Function, delay: number) {
  let timeoutId: number;
  return function (...args: any[]) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}

function App() {
  const [word, setWord] = useState("");
  const [color, setColor] = useState("gray");
  const abortController = useRef(new AbortController());

  function handleWordChange(event: React.ChangeEvent<HTMLInputElement>) {
    const newWord = event.target.value;
    setWord(newWord);
    setColor("gray");

    if (newWord === "") {
      return;
    }

    abortController.current.abort();
    abortController.current = new AbortController();
    debouncedWordExists(abortController.current.signal, newWord);
  }

  async function wordExists(signal: AbortSignal, word: string) {
    try {
      const response = await fetch(`/api/exists?word=${word}`, { signal });

      if (signal.aborted) {
        return;
      }

      if (response.status === 200) {
        setColor("success");
      } else {
        setColor("failure");
      }
    } catch (e: any) {
      if (!signal.aborted) {
        throw e;
      }
    }
  }

  const debouncedWordExists = useMemo(() => debounce(wordExists, 250), []);

  return (
    <Flowbite theme={{ theme: customTheme }}>
      <div className="w-screen">
        <div className="flex flex-col justify-start items-center gap-10 w-full">
          <nav className="bg-stone-50 drop-shadow-md w-full">
            <div className="flex place-content-center p-4">
              <span className="text-4xl font-semibold font-serif">
                Dictionary
              </span>
            </div>
          </nav>
          <div className="flex flex-col place-content-center w-3/4 max-w-7xl">
            <TextInput
              placeholder="Check word…"
              color={color}
              value={word}
              onChange={handleWordChange}
            ></TextInput>
          </div>
        </div>
      </div>
    </Flowbite>
  );
}

export default App;
