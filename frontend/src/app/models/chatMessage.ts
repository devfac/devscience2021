export class ChatMessage{
    email_from!: string;
    message!: string;
    is_ready!: boolean;
    uuid!: string
    constructor(email_from: string, message:string, is_ready: boolean, uuid: string
    ){
        this.email_from = email_from;
        this.message = message;
        this.is_ready = is_ready;
        this.uuid = uuid
    }
}
export interface Message{
    message: string,
    to?: string
}