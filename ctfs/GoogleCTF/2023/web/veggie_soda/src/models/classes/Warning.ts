import User from "./User.ts";

export default class Warning {
    public offense: string;
    public vioid: string;

    constructor(vio: string, offense: string){
        this.vioid = vio;
        this.offense = offense;
    }
    
    assign(user: User){
        user.pushToWarnings(this);
    }

    resolve(user: User): boolean{
        if (user.warnings){
            return true;
        } else return false;

    }
}