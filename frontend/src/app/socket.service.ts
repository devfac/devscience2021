import { Injectable } from "@angular/core";
import { ChatMessage, Message } from './models/chatMessage';
import { environment } from "@environments/environment";

const CHAT_URL = "ws://"+environment.socketApiURL;

@Injectable()
export class SocketService {
  webSocket!: WebSocket;
  public chatMessage: ChatMessage[] = []

  constructor(){
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
    }

    this.webSocket.onclose = (e) =>{
    }
  }

  sendMessage(chatMsg: Message){
    this.webSocket.send(JSON.stringify(chatMsg))
  }

  closeConnection(){
    this.webSocket.close()
  }

}