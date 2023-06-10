export const address = `/api`

export function headers(token){
    if(token)
        return new Headers({
        "Authorization": token,
        }); 
};
export function headersPost(token){
    return new Headers({
        "Authorization": token,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    });
}