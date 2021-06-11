package com.tenable.ctf.mvc;

public class Flag {
   private String flag;

   public void setFlag(String flag){
      this.flag  = flag;
   }
   public String getFlag(){
      return "flag{" + flag + "}";
   }
}
