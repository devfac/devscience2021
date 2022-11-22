import { Injectable } from "@angular/core";
import { ChatMessage, Message } from './models/chatMessage'

const CHAT_URL = "ws://localhost/api/v1/utils/ws/"

@Injectable()
export class SocketService {
  webSocket!: WebSocket;
  public chatMessage: ChatMessage[] = []

  constructor(){
  }


  openWebsocketConnection(id?: string, receive?: string){
    if (receive){
      console.log('avec received');
      this.webSocket =new WebSocket(CHAT_URL+id+"?client_received="+receive)
    }else{
      console.log('sans received');
      this.webSocket =new WebSocket(CHAT_URL+id)
    }


    this.webSocket.onopen = (e) => {
      console.log(e);
    }

    this.webSocket.onmessage = (e) => {
      console.log(JSON.parse(e.data));
      let chatMsg = JSON.stringify(e.data);
      this.chatMessage.push(JSON.parse(e.data))
    }

    this.webSocket.onclose = (e) =>{
      console.log(e)
    }
  }

  sendMessage(chatMsg: Message){
    this.webSocket.send(JSON.stringify(chatMsg))
  }

  closeConnection(){
    console.log('closed');
    this.webSocket.close()
  }

}