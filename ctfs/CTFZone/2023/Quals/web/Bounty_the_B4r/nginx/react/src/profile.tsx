import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Loader,
  PlusIcon,
  PlusCircleIcon,
  CircleIcon,
  StarIcon,
  ChevronDownIcon,
} from "lucide-react"
import { Separator } from "@/components/ui/separator"
import { Button } from "@/components/ui/button"
import type { User } from "./api"
import ImportReputation from "./import-rep"

type Props = {
  user: User
}

export default function Profile({ user }: Props) {
  return (
    <>
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold tracking-tight">Profile</h2>
          <p className="text-sm text-muted-foreground"></p>
        </div>
      </div>
      <Separator className="my-4" />
      <Card>
        <CardHeader className="grid grid-cols-[1fr_110px] items-start gap-4 space-y-0">
          <div className="space-y-1">
            <CardTitle>{user.username}</CardTitle>
            <CardDescription>
              Some programs are only available for users with high reputation.
              Import reputation from H1 to hit the ground running!
              Set the "Intro" field of your profile on H1 and send this string with the request for import to work.
              Your validator should be a random alphanumeric string of length 35 to prevent cheating.<b></b>
            </CardDescription>
          </div>
          <div className="flex items-center space-x-1 rounded-md bg-secondary text-secondary-foreground">
            <ImportReputation />
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-4 text-sm text-muted-foreground">
          <div>User reputation:</div>
            <div className="flex items-center">
              <StarIcon className="mr-1 h-3 w-3" />{user.reputation}
            </div>
          </div>
        </CardContent>
      </Card>
    </>
  )
}
