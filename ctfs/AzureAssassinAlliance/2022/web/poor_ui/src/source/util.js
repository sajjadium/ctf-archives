export const isJson = (s) => {
    try{
        if(JSON.parse(s) instanceof Object){ 
            return true 
        }
    }catch(e){
        // console.log(e)
    }
    return false
}