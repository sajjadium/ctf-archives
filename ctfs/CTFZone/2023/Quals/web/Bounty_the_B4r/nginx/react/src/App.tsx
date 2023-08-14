import { Redirect, Route, Switch, useRoute } from "wouter"
import { Loader } from "lucide-react"
import MainNav from "./main-nav"
import UserNav from "./user-nav"
import useUser from "./useUser"
import CreateReport from "./create-report"
import Report from "./Report"
import * as api from "./api"
import Profile from "./profile"
import Programs from "./programs"
import { useEffect, useState } from "react"
import { toast } from "./components/ui/use-toast"

export default function App() {
  const { user, isLoading } = useUser()
  const [ isReport, params ] = useRoute("/report/:id")
  const [ discoveryReport, setDiscoveryReport ] = useState<api.Report|null>(null)

  useEffect(() => {
    async function loadDiscovery() {
      try {
        const discovery = await api.getDiscovery()
        setDiscoveryReport(discovery)
      } catch(e) {
        toast({
          variant: "destructive",
          title: "Error: " + e
        })
      }
    }
    
    if (!discoveryReport) {
      loadDiscovery()
    }
  }, [])
  
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader className="animate-spin h-8 w-8" />
      </div>
    )
  }

  if (!user) {
    return <Redirect to="/login" />
  }

  return (
    <div className="hidden flex-col md:flex">
      <div className="border-b">
        <div className="flex h-16 items-center px-4">
          <MainNav className="mx-6" />
          <div className="ml-auto flex items-center space-x-4">
              {isReport === true &&
                <Report id={params!.id} pow={user.pow} md5={user.md5}/>
              }
            <CreateReport />
            <UserNav username={user.username} />
          </div>
        </div>
      </div>
      <div className="min-h-[calc(100vh-theme(spacing.16))] container mx-auto p-6">
        <Switch>
          <Route path="/profile">
            <Profile user={user} />
          </Route>
          <Route path="/programs">
            <Programs />
          </Route>
        { discoveryReport !== null &&
        <div className="grid grid-cols-4 gap-4">
          <div className="col-span-3"><b><i>The coolest recent report:</i></b></div>
          <div className="col-span-2"><b>Title</b></div>
          <div className="col-span-1"><b>Program</b></div>
          <div className="col-span-1"><b>Time</b></div>
          <div className="col-span-2">{discoveryReport.title}</div>
          <div className="col-span-1">{discoveryReport.severity}</div>
          <div className="col-span-1">{new Intl.DateTimeFormat("en-GB", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            timeZone: "UTC"
            }).format(discoveryReport.published/1000000)}.{new Date(discoveryReport.published/1000000).getUTCMilliseconds()}</div>
        </div>
        }
        </Switch>
      </div>
    </div>
  )
}
