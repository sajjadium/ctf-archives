export default interface Message {
    id: string;
    dispatch(a?: any): string;
}