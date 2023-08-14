import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { PlusCircleIcon } from "lucide-react"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { useEffect, useRef, useState } from 'react'
import { Program, createReport, getPrograms } from "./api"
import { toast } from "./components/ui/use-toast"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "./components/ui/dropdown-menu"
import { navigate } from "wouter/use-location"

export default function CreateReport() {

  const [title, setTitle] = useState<string>("")
  const [severity, setSeverity] = useState<string>("")
  const [description, setDescr] = useState<string>("")
  const [programs, setPrograms] = useState<Array<Program>>([])
  const [currentProgram, setCurrentProgram] = useState<Program>()
  const isLoading = useRef<boolean>(false);

  const onOpenChange = () => {
    setDescr("")
    setTitle("")
    setSeverity("Medium")
  }


  useEffect(() => {
    async function loadPrograms() {
      try {
        const p = await getPrograms()
        setPrograms(p)
      } catch(e) {
        toast({
          variant: "destructive",
          title: "Error: " + e
        })
      }
    }

    if (isLoading.current) {
      return
  }
    
    if (programs.length == 0) {
      isLoading.current = true
      loadPrograms()
    }
  }, [])

  //setPrograms([{id: "qwe", name: "One", type: 0}, {id: "qwe", name: "Two", type: 0}])

  const submitReport = async () => {
    try {
      const reportId = await createReport(description, title, severity, currentProgram!.id)
      navigate(`/report/${reportId}`)
    } catch(e) {
      toast({
        variant: "destructive",
        title: "Error: " + e
      })
    }
  }

  return (
    <Dialog onOpenChange={onOpenChange}>
      <DialogTrigger asChild>
        <Button variant="ghost">
          <PlusCircleIcon className="mr-2 h-4 w-4" />
          New report
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create new report</DialogTitle>
          <DialogDescription>
            Provide as much information as possible about the potential issue
            you have discovered.
          </DialogDescription>
        </DialogHeader>
        <DropdownMenu>
        <div className="grid grid-cols-4 items-center gap-4">
          <Label htmlFor="program" className="text-right">
            Programme
          </Label>
          <DropdownMenuTrigger asChild>
            <Input id="program" className="col-span-3" value={currentProgram ? currentProgram.name : ""}/>
          </DropdownMenuTrigger>
          </div>
            <DropdownMenuContent>
              {Object.values(programs).map((program) => (
                <DropdownMenuItem onClick={() => setCurrentProgram(program)}>{program.name}</DropdownMenuItem>
              ))}
            </DropdownMenuContent>
        </DropdownMenu>


        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="title" className="text-right">
              Title
            </Label>
            <Input id="title" className="col-span-3" value={title} onChange={e => setTitle(e.target.value)}/>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="severity" className="text-right">
              Severity
            </Label>
            <RadioGroup id="severity" defaultValue="comfortable">
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="default" id="r1" onClick={() => setSeverity("Low")}/>
                <Label htmlFor="r1">Low</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="comfortable" id="r2" onClick={() => setSeverity("Medium")}/>
                <Label htmlFor="r2">Medium</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="compact" id="r3" onClick={() => setSeverity("High")}/>
                <Label htmlFor="r3">High</Label>
              </div>
            </RadioGroup>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="description" className="text-right">
              Description
            </Label>
            <Textarea
              className="col-span-3"
              placeholder="Type your message here."
              id="description"
              value={description}
              onChange={e => setDescr(e.target.value)}
            />
          </div>
        </div>
        <DialogFooter>
          <Button type="submit" onClick={submitReport}>Submit</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
