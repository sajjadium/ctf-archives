#!/usr/bin/python
from ctypes import c_byte,c_ubyte,c_short,c_ushort,c_int,c_uint,c_long,c_ulong
from array import array
from time import sleep
from random import randrange
import SocketServer
from flag import secret
from curses.ascii import isprint
PORT = 1337

def delete_not_printable(s):
    return ''.join([x if isprint(x) else "" for x in s])
class CARM:
    """
    MemRange class representing one continious memory rectangle.
    Directions of reading and writing bytes in MemRange are set by the user.
    startx - the X coordinate of memory range starting address
    starty - the Y coordinate of memory range starting address
    lenx - the length of memory rectangle side parallel to the X axis
    leny - the length of memory rectangle side parallel to the Y axis
    contents - the actual array containing saved values
    restricted - determines whether addressing within one range is restrictive (trying to access something outside with directional read or writes produces and exception) or not (all reads and writes are looped inside the memory range)
    """
    class MemRange:

        
        #Simple initialization
        def __init__(self,startx,starty,lenx,leny,contents,restricted=True):
            assert(len(contents)>=(lenx*leny*2))
            contents=contents[:lenx*leny*2]
            (self.startx,self.starty,self.lenx,self.leny)=(startx,starty,lenx,leny)
            self.restricted=restricted
            
            self.contents=array('B',contents)

        #Change restriction on the go
        def setRestriction(self,restricted):
            self.restricted=restricted

        #Check if a certain address is represented inside this memory range by X and Y coordinates
        def containsAddr1(self,x,y):
            if (self.startx<=x<(self.startx+self.lenx))and (self.starty<=y<(self.starty+self.leny)):
                return True
            return False

        #Check if a register contains an address from this range
        def containsAddr2(self,reg):
            return self.containsAddr1(reg.real.value,reg.imaginary.value)

        #Get relative offset inside the range (should be used privately)
        def __getoffset(self,reg):
            (sx,sy)=(reg.real.value-self.startx,reg.imaginary.value-self.starty)
            return (sx,sy)

        #Get single byte at relative offset (should be used privately)
        def __getbytebyoffset(self,x,y):
            return (self.contents[(x+self.lenx*y)*2],self.contents[(x+self.lenx*y)*2+1])

        #Set single byte at relative offset (should be used privately)
        def __setbytebyoffset(self,x,y,r,i):
            (self.contents[(x+self.lenx*y)*2],self.contents[(x+self.lenx*y)*2+1])=(r,i)
        #Convert directional sequence of bytes in the range into an integer for transfer
        def getSequence(self,reg,direction,steps):
            assert(direction!=CARM.REG(0,0))
            (dirx,diry)=(direction.real.value,direction.imaginary.value)
            if not self.containsAddr2(reg):
                raise Exception("Memory access error\n")
            (x1,y1)=self.__getoffset(reg)
            
            (x_full,y_full)=(0,0)
            for i in range(0,steps):
                if self.restricted:
                    if x1>=self.lenx or y1>=self.leny or x1<0 or y1<0:
                        raise Exception("Memory access error\n")
                else:
                    (x1,y1)=(x1%self.lenx,y1%self.lenx)
                (x_cur,y_cur)=self.__getbytebyoffset(x1,y1)
                (x_full,y_full)=(x_full|x_cur<<(8*i),y_full|y_cur<<(8*i))
                (x1,y1)=(x1+dirx,y1+diry)
            return (x_full,y_full)
        
        def __setsequence(self,reg,direction,r,im,steps):
            assert(direction!=CARM.REG(0,0))
            (dirx,diry)=(direction.real.value,direction.imaginary.value)
            if not self.containsAddr2(reg):
                raise Exception("Memory access error\n")
            (x1,y1)=self.__getoffset(reg)
            
            
            for i in range(0,steps):
                if self.restricted:
                    if x1>=self.lenx or y1>=self.leny or x1<0 or y1<0:
                        raise Exception("Memory access error\n")
                else:
                    (x1,y1)=(x1%self.lenx,y1%self.lenx)
                self.__setbytebyoffset(x1,y1,r&0xff,im&0xff)
                (r,im)=(r>>8,im>>8)
                (x1,y1)=(x1+dirx,y1+diry)
        def writeMemory(self,reg,direction,data,steps):
            assert(direction!=CARM.REG(0,0))
            (dirx,diry)=(direction.real.value,direction.imaginary.value)
            if not self.containsAddr2(reg):
                raise Exception("Memory access error\n")
            (x1,y1)=self.__getoffset(reg)
            
            
            for i in range(0,steps):
                if self.restricted:
                    if x1>=self.lenx or y1>=self.leny or x1<0 or y1<0:
                        raise Exception("Memory access error\n")
                else:
                    (x1,y1)=(x1%self.lenx,y1%self.lenx)
                self.__setbytebyoffset(x1,y1,ord(data[i*2]),ord(data[i*2+1]))
                #(r,im)=(r>>8,im>>8)
                (x1,y1)=(x1+dirx,y1+diry)

        def readMemory(self,reg,direction,steps):
            assert(direction!=CARM.REG(0,0))
            s=''
            (dirx,diry)=(direction.real.value,direction.imaginary.value)
            if not self.containsAddr2(reg):
                raise Exception("Memory access error\n")
            (x1,y1)=self.__getoffset(reg)
            
            
            for i in range(0,steps):
                if self.restricted:
                    if x1>=self.lenx or y1>=self.leny or x1<0 or y1<0:
                        raise Exception("Memory access error\n")
                else:
                    (x1,y1)=(x1%self.lenx,y1%self.lenx)
                (a,b)=self.__getbytebyoffset(x1,y1)
                s+=chr(a)+chr(b)
                #(r,im)=(r>>8,im>>8)
                (x1,y1)=(x1+dirx,y1+diry)     
            return s
        #Load one BYTE with zero extension
        def getZBYTE(self,reg,direction):
            (x,y)=self.getSequence(reg,direction,1)
            return CARM.REG(x,y)
        #Load one BYTE with sign extension
        def getSBYTE(self,reg,direction):
            (x,y)=self.getSequence(reg,direction,1)
            (x,y)=((1<<32-(x&1<<7))|x,(1<<32-(y&1<<7))|y)
            return CARM.REG(x,y)
        #Load one WORD with zero extension
        def getZWORD(self,reg,direction):
            (x,y)=self.getSequence(reg,direction,2)
            return CARM.REG(x,y)
        #Load one WORD with sign extension
        def getSWORD(self,reg,direction):
            (x,y)=self.getSequence(reg,direction,2)
            (x,y)=((1<<32-(x&1<<15))|x,(1<<32-(y&1<<15))|y)
            return CARM.REG(x,y)
        #Load one DWORD
        def getDWORD(self,reg,direction):
            (x,y)=self.getSequence(reg,direction,4)
            return CARM.REG(x,y)
        
        def setBYTE(self,reg,direction,val_reg):
            self.__setsequence(reg,direction,val_reg.real.value,val_reg.imaginary.value,1)

        def setWORD(self,reg,direction,val_reg):
            self.__setsequence(reg,direction,val_reg.real.value,val_reg.imaginary.value,2)

        def setDWORD(self,reg,direction,val_reg):
            self.__setsequence(reg,direction,val_reg.real.value,val_reg.imaginary.value,4)

        def nextAddress(self,reg,direction):
            assert(direction!=CARM.REG(0,0))
            if self.restricted:
                if self.containsAddr2(reg+direction):
                    return reg+direction
                else:
                    raise Exception("Illegal address")
            else:
                return CARM.REG((reg.real.value-self.startx+direction.real.value)%self.lenx+self.startx,(reg.imaginary.value-self.starty+direction.imaginary.value)%self.leny+self.starty)

               
            
    class REG:
        def __init__(self,r=0,i=0):
            self.real=c_uint(r)
            self.imaginary=c_uint(i)
        def __add__(self,other):
            return CARM.REG(self.real.value+other.real.value,self.imaginary.value+other.imaginary.value)
        def __radd__(self,other):
            return self.__add__(other)
        def __mul__(self,other):
            return CARM.REG(self.real.value*other.real.value-self.imaginary.value*other.imaginary.value,self.real.value*other.imaginary.value+self.imaginary.value*other.real.value)
        def __rmul__(self,other):
            return self.__mul__(other)
        def __xor__(self, other):
            return CARM.REG(self.real.value^other.real.value,self.imaginary.value^other.imaginary.value)
        def __sadd__(self,other):
            (r1,i1,r2,i2)=(self.real.value,self.imaginary.value,other.real.value,other.imaginary.value)
            (r1,i1,r2,i2)=(r1 if r1<(1<<31) else r1-(1<<32),i1 if i1<(1<<31) else i1-(1<<32),r2 if r2<(1<<31) else r2-(1<<32),i2 if i2<(1<<31) else i2-(1<<32))
            return CARM.REG(r1+r2,i1+i2)
        def __str__(self):
            return '( '+hex(self.real.value)[:-1]+' + '+hex(self.imaginary.value)[:-1]+'i )'
        def div_real(self,numb):
            return CARM.REG(self.real.value/numb,self.imaginary.value/numb)
        def __div__(self,other):
            if other.real.value==0 and other.imaginary.value==0:
                raise Exception("Can't divide by null")
            (r1,i1,r2,i2)=(self.real.value,self.imaginary.value,other.real.value,other.imaginary.value)
            (r1,i1,r2,i2)=(r1 if r1<(1<<31) else r1-(1<<32),i1 if i1<(1<<31) else i1-(1<<32),r2 if r2<(1<<31) else r2-(1<<32),i2 if i2<(1<<31) else i2-(1<<32))
            (r_f,i_f)=(r1*r2+i1*i2,-r1*i2+i1*r2)
            
            divis=(r2**2+i2**2)
            
            return CARM.REG(r_f/divis,i_f/divis)
        def __ovf__(self,other):
            return CARM.REG(self.real.value%other.real.value,self.imaginary.value%other.imaginary.value)
        def __neg__(self):
            return CARM.REG(-self.real.value,-self.imaginary.value)
        def __sub__(self,other):
            return self.__add__(other.__neg__())
       
        @staticmethod
        def toSigned(num):
            return num if num<(1<<31) else num-(1<<32)
            
        def real_above(self,other):
            return self.real.value>other.real.value
        def real_below(self,other):
            return self.real.value<other.real.value
        def real_equal(self,other):
            return self.real.value==other.real.value
        def real_more(self,other):
            return CARM.REG.toSigned(self.real.value)>CARM.REG.toSigned(other.real.value)
        def real_less(self,other):
            return CARM.REG.toSigned(self.real.value)<CARM.REG.toSigned(other.real.value)
        def imaginary_above(self,other):
            return self.imaginary.value>other.imaginary.value
        def imaginary_below(self,other):
            return self.imaginary.value<other.imaginary.value
        def imaginary_equal(self,other):
            return self.imaginary.value==other.imaginary.value
        def imaginary_more(self,other):
            return CARM.REG.toSigned(self.imaginary.value)>CARM.REG.toSigned(other.imaginary.value)
        def imaginary_less(self,other):
            return CARM.REG.toSigned(self.imaginary.value)<CARM.REG.toSigned(other.imaginary.value)
        def __eq__(self,other):
            return self.real.value==other.real.value and self.imaginary.value==other.imaginary.value
        def __ne__(self,other):
            return not self.__eq__(other)
        def __mod__(self,other):
            return self.__ovf__(other)
        def __lt__(self,other):
            return self.real.value<other.real.value and self.imaginary.value<other.imaginary.value
        def __le__(self,other):
            return self.real.value<=other.real.value and self.imaginary.value<=other.imaginary.value
        def __gt__(self,other):
            return self.real.value>other.real.value and self.imaginary.value>other.imaginary.value
        def __ge__(self,other):
            return self.real.value>=other.real.value and self.imaginary.value>=other.imaginary.value
       
    
    #commands=[0x20,]
    #hadlers=[self.nop]
    def __initializeprogrammemory(self):
        self.memory=[
            #CARM.MemRange(0x40000,0x40000,30,10,"0\x10\x49\x01 \x01\x00"+" \x01"*600),   #Executable code
            CARM.MemRange(0x60000,0x60000,300,1,
            "\x45\x00\x06\x00\x00\x00\x06\x06\x00\x00"+
            "\x00\x00"+
            "\x31\x05\x40\x40\x00\x00\x06\x06\x00\x00"+
            "\x31\x03\x04\x00\x00\x00\x00\x00\x00\x00"+
            "\x31\x06\x01\x00\x00\x00\x00\x00\x00\x00"+
            "\x49\x03"+

            "\x31\x05\x40\x41\x00\x00\x06\x06\x00\x00"+
            "\x31\x03\x09\x00\x00\x00\x00\x00\x00\x00"+
            "\x49\x03"+
            "\x31\x04\x40\x45\x00\x00\x06\x06\x00\x00"+
            "\x31\x01\x00\x01\x00\x00\x00\x00\x00\x00"+
            "\x49\x05"+#68
            
            "\x31\x05\x40\x42\x00\x00\x06\x06\x00\x00"+
            "\x31\x03\x09\x00\x00\x00\x00\x00\x00\x00"+
            "\x49\x03"+
            
            "\x41\x45"+
            "\x31\x03\x10\x00\x00\x00\x00\x00\x00\x00"+
            "\x49\x02"+
            "\x30\x14"
            "\x47\x00\x2c\x00\x00\x00\x06\x06\x00\x00"+
            
            "\x31\x05\x40\x43\x00\x00\x06\x06\x00\x00"+
            "\x31\x03\x09\x00\x00\x00\x00\x00\x00\x00"+
            "\x49\x03"+

            "\x49\x05"+

            "\x31\x05\x40\x44\x00\x00\x06\x06\x00\x00"+
            "\x31\x03\x10\x00\x00\x00\x00\x00\x00\x00"+
            "\x49\x03"+

            "\x48\x07\x10\x00\x00\x00\x00\x00\x00\x00"+
            "\x41\x75"+
            "\x41\x23"
            "\x49\x02"+
            "\x49\x03"+
            "\x48\x07\xf0\x00\xff\x00\xff\x00\xff\x00"+
            "\x46\x00"+
             "\x01"*600),   #Executable code
            CARM.MemRange(0x60000,0x60001,0x100,1,"\x00"*800),                             #Stack
            CARM.MemRange(0x60040,0x60040,0x10,0x40,"EasyPwn"+"\x00"*0x19+ #16
            "How many strings:" +"\x00"*0xf+ #14
            "Input: "+"\x00"*0x19+#8
            "How many letters:"+"\x00"*0xf+
            "Your name please:"+"\x00"*0x0f+#8
            "\x00"*0x1000)                              #data
            ]
    
    def __initializeregisters(self):
        self.eax=CARM.REG(0,0)
        self.ebx=CARM.REG(0,0)
        self.ecx=CARM.REG(0,0)
        self.edx=CARM.REG(0,0)
        self.esi=CARM.REG(0,0)
        self.edi=CARM.REG(0,0)
        self.edid=CARM.REG(0,0)
        self.esd=CARM.REG(0,0)
        self.edd=CARM.REG(0,0)
        self.esp=CARM.REG(0x60100,0x60001)
        self.espd=CARM.REG(1,0)
        self.eip=CARM.REG(0x60000,0x60000)
        self.eipd=CARM.REG(1,0)
        self.dataregs=[self.eax,self.ebx,self.ecx,self.edx,self.esi,self.edi,self.edid,self.esp]
        self.ZF=False;
        self.CF=False;
        self.SF=False;
        self.OF=False;
        self.NO=False;
        
    def __update_states(self):
        (self.eax,self.ebx,self.ecx,self.edx,self.esi,self.edi,self.edid,self.esp)=self.dataregs
    def __update_states1(self):
        self.dataregs=[self.eax,self.ebx,self.ecx,self.edx,self.esi,self.edi,self.edid,self.esp]
    def __init__(self,socket):
        self.socket=socket.request
        self.__initializeregisters()
        self.__initializeprogrammemory()
        self.commands={
             0x00:  self.__command_powerdown,
             
             0x20:  self.__command_nop,
             0x30:  self.__command_add,
             0x31:  self.__command_mov_data,
             0x32:  self.__command_xor,
             0x33:  self.__command_rotip,
             0x40:  self.__command_test,
             0x41:  self.__command_mov_reg,
             0x42:  self.__command_mov_data_to_reg,
             0x43:  self.__command_mov_data_from_reg,
             0x45:  self.__command_call,
             0x46:  self.__command_ret,
             0x47:  self.__command_jmpne,
             0x48:  self.__command_sub,
             0x49:  self.__command_syscall,
             0x50:  self.__command_switch,}
    """
    ===================
    =Commands' section=
    ===================
    """
    #No Operation
    def __command_nop(self,amplifier=0):
        for mrange in self.memory:
            if mrange.containsAddr2(self.eip):
                self.eip=mrange.nextAddress(self.eip,self.eipd)
                return
        raise Exception("Eip not in identifiable memory range\n")

    #Shut the emulator down
    def __command_powerdown(self,amplifier=0):
        
        return True

    #Register addtition
    def __command_add(self,amplifier):
        inreg=amplifier&0xf
        outreg=amplifier>>4
        if inreg>len(self.dataregs) or outreg>len(self.dataregs):
            raise Exception("Illegal command\n")
        self.dataregs[inreg]=self.dataregs[inreg]+self.dataregs[outreg]
        self.__update_states()
        self.__command_nop()

    def __command_xor(self,amplifier):
        inreg=amplifier&0xf
        outreg=amplifier>>4
        if inreg>len(self.dataregs) or outreg>len(self.dataregs):
            raise Exception("Illegal command\n")
        self.dataregs[inreg]=self.dataregs[inreg].__xor__(self.dataregs[outreg])
        self.__update_states()
        self.__command_nop()

    def __command_switch(self,amplifier):
        inreg=amplifier&0xf
        if inreg>len(self.dataregs):
            raise Exception("Illegal command\n")
        
        self.dataregs[inreg]=CARM.REG(self.dataregs[inreg].imaginary.value,self.dataregs[inreg].real.value)
        self.__update_states()
        self.__command_nop()

    #Register addtition
    def __command_mov_reg(self,amplifier):
        inreg=amplifier&0xf
        outreg=amplifier>>4
        if inreg>len(self.dataregs) or outreg>len(self.dataregs):
            raise Exception("Illegal command\n")
        self.dataregs[inreg]=self.dataregs[outreg]
        self.__update_states()
        self.__command_nop()

    #JUMP to Address
    def __command_jump_basic(self,amplifier=0):
        self.__command_nop()
        for mrange in self.memory:
            if mrange.containsAddr2(self.eip):
                self.eip=mrange.getDWORD(self.eip,self.eipd)
                return
        raise Exception("Nowhere to jump")

    #Register multiplication
    def __comand_mul(self,amplifier):
        inreg=amplifier&0xf
        outreg=amplifier>>4
        if inreg>len(self.dataregs) or outreg>len(self.dataregs):
            raise Exception("Illegal command\n")
        self.dataregs[inreg]=self.dataregs[inreg]*self.dataregs[outreg]
        self.__update_states()
        self.__command_nop()
    """
    def movd(self,amplifier):
        inreg=amplifier&0xf
        outreg=amplifier>>4
        if inreg>len(self.dataregs) or outreg>1:
            raise Exception("Illegal command\n")
        if outreg==1:
            array[]
    """

    def __getMrange(self,reg):
        for i in range(0,len(self.memory)):
            if self.memory[i].containsAddr2(reg):
                return i
        raise Exception("Register not in any memory range")
    def __command_call(self,amplifier):
        self.__command_nop()
        reg=self.memory[self.__getMrange(self.eip)].getDWORD(self.eip,self.eipd)
        self.esp=CARM.REG(self.esp.real.value-4,self.esp.imaginary.value)
        self.__command_nop()
        self.__command_nop()
        self.__command_nop()
        self.__command_nop()
        self.memory[self.__getMrange(self.esp)].setDWORD(self.esp,self.espd,self.eip)
        self.eip=reg
        self.__update_states1()

    
    def __command_sub(self,amplifier):
        self.__command_nop()
        inreg=amplifier&0xf
        
        if inreg>len(self.dataregs):
            raise Exception("Illegal command\n")
        reg=self.memory[self.__getMrange(self.eip)].getDWORD(self.eip,self.eipd)
        self.esp=self.esp-reg
        #self.esp=CARM.REG(self.esp.real.value-4,self.esp.imaginary.value)
        
        self.__command_nop()
        self.__command_nop()
        self.__command_nop()
        self.__command_nop()
        
        self.__update_states1()
        
        
        
    
    def __command_jmpne(self,amplifier):
        self.ecx=CARM.REG(self.ecx.real.value-1,self.ecx.imaginary.value)
        self.__command_nop()
        if self.ecx.real.value!=0:
            
            reg=self.memory[self.__getMrange(self.eip)].getDWORD(self.eip,self.eipd)
        
            self.eip=reg
        else:
            self.__command_nop()
            self.__command_nop()
            self.__command_nop()
            self.__command_nop()
        self.__update_states1()
        
        
      

    def __command_ret(self,amplifier):
        self.__command_nop()
        self.eip=self.memory[self.__getMrange(self.esp)].getDWORD(self.esp,self.espd)
        self.esp=CARM.REG(self.esp.real.value+4,self.esp.imaginary.value)

    def __command_rotip(self,amplifier):
        self.__command_nop()
        if amplifier&1:
            self.eipd=self.eipd*CARM.REG(0,1)
        else:
            self.eipd=self.eipd*CARM.REG(0,-1)
        
    def __command_mov_data(self,amplifier):
        inreg=amplifier&0xf
        tp=amplifier>>4
        if inreg>len(self.dataregs):
            raise Exception("Illegal command\n")
        self.__command_nop()
        if (tp&1)==0:
            self.dataregs[inreg]=self.memory[self.__getMrange(self.eip)].getDWORD(self.eip,self.eipd)
            self.__update_states()
            self.__command_nop()
            self.__command_nop()
            self.__command_nop()
            self.__command_nop()
        else:
            reg=self.memory[self.__getMrange(self.eip)].getDWORD(self.eip,self.eipd)
            self.__command_nop()
            self.__command_nop()
            self.__command_nop()
            self.__command_nop()
            drctn=self.memory[self.__getMrange(self.eip)].getDWORD(self.eip,self.eipd)
            self.dataregs[inreg]=self.memory[self.__getMrange(reg)].getDWORD(reg,drctn)
            self.__update_states()
            self.__command_nop()
    def __command_mov_data_to_reg(self,amplifier):
        inreg=amplifier&0xf
        tp=amplifier>>4
        if inreg>len(self.dataregs) or tp>len(self.dataregs):
            raise Exception("Illegal command\n")
        self.__command_nop()
        regd=self.memory[self.__getMrange(self.eip)].getZBYTE(self.eip,self.eipd)
        self.dataregs[inreg]=self.memory[self.__getMrange(self.dataregs[tp])].getDWORD(self.dataregs[tp],regd)
        self.__update_states()
        self.__command_nop()
    def __command_mov_data_from_reg(self,amplifier):
        inreg=amplifier&0xf
        tp=amplifier>>4
        if inreg>len(self.dataregs) or tp>len(self.dataregs):
            raise Exception("Illegal command\n")
        self.__command_nop()
        regd=self.memory[self.__getMrange(self.eip)].getZBYTE(self.eip,self.eipd)
        #self.dataregs[inreg]=self.memory[self.__getMrange(self.dataregs[tp])].getDWORD(self.dataregs[tp],regd)
        self.memory[self.__getMrange(self.dataregs[inreg])].setDWORD(self.dataregs[inreg],regd,self.dataregs[tp])
        self.__update_states()
        self.__command_nop()
        
        
    #Calling system functions
    def __command_syscall(self,amplifier):
        if amplifier==1:
            self.socket.sendall(str(self.eax)+'\n')
            
        elif amplifier==2:
            s=delete_not_printable(self.socket.recv(64))
            self.memory[self.__getMrange(self.edi)].writeMemory(self.edi,self.edid,s,self.edx.real.value)
        elif amplifier==3:
            s=self.memory[self.__getMrange(self.edi)].readMemory(self.edi,self.edid,self.edx.real.value)
            self.socket.sendall(s+'\n')
        elif amplifier==4:
            data=""
            for i in range(0,self.edx.real.value*2):
                data+=chr(randrange(self.ecx.real.value,self.ecx.imaginary.value))
            self.memory[2].writeMemory(self.edi,self.edid,data,self.edx.real.value)
        elif amplifier==5:
            data=int(self.socket.recv(64))
            self.ecx=CARM.REG(data,0)
            self.__update_states1()
        
        elif amplifier==0x40:
            if (self.eax==CARM.REG(ord("f"),ord("l"))) and (self.ebx==CARM.REG(ord("a"),ord("g"))):
                self.socket.sendall(secret+'\n')
        
        else:
            raise Exception("Illegal command\n")
        self.__command_nop()

    def __command_test(self,amplifier):
        inreg=amplifier&0xf
        outreg=amplifier>>4
        if inreg>len(self.dataregs) or outreg>len(self.dataregs):
            raise Exception("Illegal command\n")
        (first,second)=(self.dataregs[inreg],self.dataregs[outreg])
        self.ZF=(first==second)

        self.__update_states()
        self.__command_nop()

    def __getcommand(self):
        for mrange in self.memory:
            if mrange.containsAddr2(self.eip):
                byte=mrange.getZBYTE(self.eip,self.eipd)

    def processComand(self):
        defaultMrange=None
        for mrange in self.memory:
            if mrange.containsAddr2(self.eip):
                defaultMrange=mrange
                break
        if defaultMrange==None:
            
            raise Exception("EIP not in identifiable range")
        commandByte=defaultMrange.getZBYTE(self.eip,self.eipd)
        (opcode,amplifier)=(commandByte.real.value,commandByte.imaginary.value)
        
        if opcode in self.commands.keys():
            return self.commands[opcode](amplifier)
        else:
            raise Exception("Illegal command\n")
    def run(self):
        pwd=None
        while pwd!=True:
            pwd=self.processComand()
    

command_prefixes=[]
handlers=[]
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
  
  def handle(self):
    try:
        emulator=CARM(self)
        emulator.run()
    except Exception,e:
        ret ='Error: ' +str(e)
    self.request.sendall(ret+'\n')
 

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  pass

if __name__ == '__main__':
  
  server = ThreadedTCPServer(('0.0.0.0', PORT), ThreadedTCPRequestHandler)
  server.allow_reuse_address = True
  server.serve_forever()