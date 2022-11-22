export interface Permission{
    uuid: string,
    email: string,
    email_sender: string,
    accepted: boolean,
    valid_time: number,
    type: string
}