import { Separator } from "@/components/ui/separator"
import { Button } from "@/components/ui/button"
import { getPrograms, joinProgram, type Program } from "./api"
import { useEffect, useRef, useState } from "react"
import { toast } from "./components/ui/use-toast"
  
  
  export default function Programs() {
    const [programs, setPrograms] = useState<Array<Program>>([])
    const isLoading = useRef<boolean>(false);

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

    const join = async (p: string) => {
        try {
            await joinProgram(p)
            setPrograms(await getPrograms())
          } catch(e) {
            toast({
              variant: "destructive",
              title: "Error: " + e
            })
          }
    }
    
    return (
      <>
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <h2 className="text-2xl font-semibold tracking-tight">Programs</h2>
            <p className="text-sm text-muted-foreground"></p>
          </div>
        </div>
        <Separator className="my-4" />
        <div className="grid grid-cols-4 gap-4">
          <div className="col-span-2"><b>Name</b></div>
          <div className="col-span-1"><b>Status</b></div>
          <div className="col-span-1"><b>Join</b></div>
          {Object.values(programs).map((program) => (
            <>
            <div className="col-span-2">{program.name}</div>
            <div className="col-span-1">{program.programType == 0 ? "Public" : "Private"}</div>
            <div className="col-span-1">
            {program.joined ?
              <Button disabled={true}>Joined</Button> :
              <Button type="submit" onClick={() => join(program.id)}>Join</Button>
            }</div>
            </>
          ))}
          
        </div>
      </>
    )
  }
  