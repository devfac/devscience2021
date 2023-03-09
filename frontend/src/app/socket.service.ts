import { Injectable } from "@angular/core";
import { ChatMessage, Message } from './models/chatMessage'
import { environment } from "@environments/environment";
import { NzNotificationPlacement, NzNotificationService } from "ng-zorro-antd/notification";

const CHAT_URL = environment.socketApiURL

@Injectable()
export class SocketService {
  webSocket!: WebSocket;
  public chatMessage: ChatMessage[] = []

  constructor(private notification: NzNotificationService){
  }


  openWebsocketConnection(id?: string, receive?: string){
    if (receive){
      this.webSocket =new WebSocket(CHAT_URL+id+"?client_received="+receive)
    }else{
      this.webSocket =new WebSocket(CHAT_URL+id)
    }

   

    this.webSocket.onopen = (e) => {
      console.log(e);
    }

    this.webSocket.onmessage = (e) => {
      let chatMsg = JSON.stringify(e.data);
      this.chatMessage.push(JSON.parse(e.data))
      this.createBasicNotification("bottomRight", JSON.parse(e.data))
    }

    this.webSocket.onclose = (e) =>{
    }
  }

  createBasicNotification(position: NzNotificationPlacement, message: any): void {
    if (!message.is_ready){
      console.log( message);
      this.notification.blank(
        message.email_from,
        message.message,
        { nzPlacement: position }
      );
    }
  }

  createNotification(position: NzNotificationPlacement, message: string, title: string): void {
      this.notification.blank(
        title,
        message,
        { nzPlacement: position }
      );
  }
  
  sendMessage(chatMsg: Message){
    this.webSocket.send(JSON.stringify(chatMsg))
  }

  closeConnection(){
    this.webSocket.close()
  }

}