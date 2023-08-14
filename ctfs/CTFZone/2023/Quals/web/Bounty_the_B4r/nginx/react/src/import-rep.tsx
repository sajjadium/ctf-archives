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
import { Label } from "@/components/ui/label"
import { StarIcon } from "lucide-react"
import { useState } from 'react'
import * as api from "./api"
import { toast } from "./components/ui/use-toast"

export default function ImportReputation() {

  const [username, setUsername] = useState<string>("")
  const [validator, setValidator] = useState<string>("")
  const [open, setOpen] = useState<boolean>(false)

  const onOpenChange = (o: boolean) => {
    setOpen(o)
    setUsername("")
    setValidator("")
  }

  const importRepo = async () => {
    try {
      await api.importReputation(username, validator)
      setOpen(false)
    } catch(e) {
      toast({
        variant: "destructive",
        title: "Error: " + e
      })
    }
  }

  return (
    <Dialog onOpenChange={onOpenChange} open={open} >
      <DialogTrigger asChild>
        <Button variant="secondary">
          <StarIcon className="mr-2 h-4 w-4" />
          Import
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Import reputation</DialogTitle>
          <DialogDescription>
            Make sure your validator matches your info on H1
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="title" className="text-right">
              H1 Username
            </Label>
            <Input id="title" className="col-span-3" value={username} onChange={e => setUsername(e.target.value)}/>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="title" className="text-right">
              Validator
            </Label>
            <Input id="title" className="col-span-3" value={validator} onChange={e => setValidator(e.target.value)}/>
          </div>
        </div>
        <DialogFooter>
          <Button type="submit" onClick={importRepo}>Submit</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
