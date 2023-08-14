import {
  createContext,
  useState,
  useEffect,
  useContext,
  ReactNode,
} from "react"
import { User, getUser } from "./api"

type Context = {
  user?: User
  isLoading: boolean
  fetchUser: () => Promise<void>
}

const UserContext = createContext<Context>({
  isLoading: false,
  fetchUser: () => Promise.resolve(),
})

type Props = {
  children: ReactNode
}

export function UserContextProvider({ children }: Props) {
  const [user, setUser] = useState<User | undefined>(undefined)
  const [isLoading, setIsLoading] = useState(true)

  const fetchUser = async () => {
    try {
      const user = await getUser()
      setUser(user)
    } catch (e) {
      setUser(undefined)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchUser()
  }, [])

  const context = {
    user,
    isLoading,
    fetchUser,
  }

  return <UserContext.Provider value={context}>{children}</UserContext.Provider>
}

export default function useUser() {
  const context = useContext(UserContext)

  if (context === undefined) {
    throw new Error("userUser was used outside of its Provider")
  }

  return context
}
