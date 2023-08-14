import { useState, FormEvent } from "react"
import { Loader } from "lucide-react"
import { Link, useLocation } from "wouter"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { login, register } from "./api"
import { useToast } from "@/components/ui/use-toast"
import useUser from "./useUser"

interface Props {
  type: "login" | "registration"
}

export default function Auth({ type }: Props) {
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const { toast } = useToast()
  const [_, navigate] = useLocation()
  const { fetchUser } = useUser()

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsLoading(true)

    const target = event.target as typeof event.target & {
      username: { value: string }
      password: { value: string }
    }

    try {
      if (type === "registration") {
        await register(target.username.value, target.password.value)
      } else {
        await login(target.username.value, target.password.value)
      }
      await fetchUser()
      navigate("/")
    } catch (e: any) {
      toast({
        variant: "destructive",
        title: "Something went wrong.",
        description: e.message,
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <div className="mx-auto flex w-full h-screen flex-col justify-center p-2 space-y-6 sm:w-[350px]">
        <div className="flex flex-col space-y-2 text-center">
          <h1 className="text-2xl font-semibold tracking-tight">
            {type == "registration"
              ? "Create an account"
              : "Login into your account"}
          </h1>
        </div>{" "}
        <div className="grid gap-6">
          <form onSubmit={onSubmit}>
            <div className="grid gap-6">
              <div className="grid gap-1">
                <Label className="sr-only" htmlFor="email">
                  Email
                </Label>
                <Input
                  id="username"
                  name="username"
                  placeholder="email"
                  type="text"
                  autoCapitalize="none"
                  autoCorrect="off"
                  disabled={isLoading}
                />
                <Input
                  id="password"
                  placeholder="password"
                  name="password"
                  type="password"
                  disabled={isLoading}
                />
              </div>
              <Button disabled={isLoading}>
                {isLoading && <Loader className="mr-2 h-4 w-4 animate-spin" />}
                {type == "registration" ? "Sign Up" : "Sign In"}
              </Button>
            </div>
          </form>
        </div>
        {type == "registration" ? (
          <p className="px-8 text-center text-sm text-muted-foreground">
            Already have an account?{" "}
            <Link
              href="/login"
              className="underline underline-offset-4 hover:text-primary"
            >
              Login
            </Link>
          </p>
        ) : (
          <p className="px-8 text-center text-sm text-muted-foreground">
            Don't have an account?{" "}
            <Link
              href="/register"
              className="underline underline-offset-4 hover:text-primary"
            >
              Register
            </Link>
          </p>
        )}
      </div>
    </>
  )
}
