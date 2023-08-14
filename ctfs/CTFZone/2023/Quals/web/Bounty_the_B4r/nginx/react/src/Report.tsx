import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Loader, PlusCircleIcon } from "lucide-react"
import { useContext, useEffect, useRef, useState } from 'react'
import { getReport, Report } from "./api"
import { toast } from "./components/ui/use-toast"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "./components/ui/dropdown-menu"
import { navigate } from "wouter/use-location"


type Props = {
    id: string
    pow: string
    md5: string
}

export default function Report({ id, pow, md5 }: Props) {
  const [report, setReport] = useState<Report|null>(null);
  const [powInput, setPowInput] = useState<string>("");
  const powEntered = useRef<Boolean>(false);

  return (
    <Dialog open={true}>
      <DialogContent className="sm:max-w-[425px]">
        { powEntered.current ?
        <>
        <DialogHeader>
          <DialogTitle>View report</DialogTitle>
          <DialogDescription>
            See report details
          </DialogDescription>
        </DialogHeader>
        <DropdownMenu>
        <div className="grid grid-cols-4 items-center gap-4">
          <Label htmlFor="program" className="text-right">
            Programme
          </Label>
          <DropdownMenuTrigger asChild>
            <Input id="program" disabled={true} className="col-span-3" value={report?.programName}/>
          </DropdownMenuTrigger>
          </div>
        </DropdownMenu>


        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="title" className="text-right">
              Title
            </Label>
            <Input id="title" disabled={true} className="col-span-3" value={report?.title}/>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="severity" className="text-right">
              Severity
            </Label>
            <Input id="severity" disabled={true} className="col-span-3" value={report?.severity}/>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="description" className="text-right">
              Description
            </Label>
            <Textarea
              disabled={true}
              className="col-span-3"
              placeholder="Type your message here."
              id="description"
              value={report?.description}
            />
          </div>
        </div>
        <DialogFooter>
          <Button type="submit" onClick={() => navigate("/")}>Close</Button>
        </DialogFooter>
        </> : 
        <>
        <DialogHeader>
          <DialogTitle>Proof of work check</DialogTitle>
          <DialogDescription>
            Send the original string (starts with {pow}....) such as {"\n"}
            md5({pow}....) = {md5}
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="title" className="text-right">
              String
            </Label>
            <Input id="title" className="col-span-3" value={powInput} onChange={e => setPowInput(e.target.value)}/>
          </div>
        </div>
        <DialogFooter>
          <Button type="submit" onClick={() => {
            getReport(id, powInput).
            then((r) => {
              setReport(r);
              powEntered.current = true
            }).catch((e) => {
              toast({
                variant: "destructive",
                title: "Error: " + e
              })
            })}
          }>Submit</Button>
        </DialogFooter>
        </>
      }
      </DialogContent>
    </Dialog>
  )
}
