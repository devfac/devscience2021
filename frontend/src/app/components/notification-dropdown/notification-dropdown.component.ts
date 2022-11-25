import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ChatMessage } from '@app/models/chatMessage';
import { AuthService } from '@app/services/auth/auth.service';
import { SocketService } from '@app/socket.service';
import { environment } from '@environments/environment';

const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-notification-dropdown',
  templateUrl: './notification-dropdown.component.html',
  styleUrls: ['./notification-dropdown.component.less'],
})
export class NotificationDropdownComponent implements OnInit {
  notifcationsDrawerVisible = false;
  numberOfUnread: number = 2;
  isvisible: boolean = false;
  invitation! : ChatMessage

  constructor(
    public socketService: SocketService,
    private authUser: AuthService,private http: HttpClient ) {
    ;
  }
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  ngOnInit(): void {
    const user = this.authUser.userValue
    this.socketService.openWebsocketConnection(user?.email)
  }

  async updateData(uuid: string){
    const body = {
      is_ready: true
    }
    const invitation: ChatMessage = await this.http.put<ChatMessage>(`${BASE_URL}/invitation/?uuid=`+uuid, body, {headers: this.headers}).toPromise()
    const index = this.socketService.chatMessage.findIndex((item) => item.uuid === uuid);
    this.socketService.chatMessage[index] = invitation
    if (invitation){
      this.invitation = invitation
      this.isvisible = true
    }
  }

  async deleteData(uuid: string){

    const invitation: ChatMessage = await this.http.delete<ChatMessage>(`${BASE_URL}/invitation/?uuid=`+uuid, {headers: this.headers}).toPromise()
    this.socketService.chatMessage = this.socketService.chatMessage.filter((item) => item.uuid !== uuid)
  }

  bodyStyle = {
    padding: 0,
    margin: 0,
  }

  unreadNotification():number{
    let nbr = 0
    for(let i=0; i<this.socketService.chatMessage.length; i++){
      if (!this.socketService.chatMessage[i].is_ready){
          nbr += 1
      }
    }
    return nbr
  }

  showNotificationDrawer() {
    this.notifcationsDrawerVisible = true;
  }

  closeNotificationDrawer() {
    this.notifcationsDrawerVisible = false;
  }

  maxLenthText(value: string): string{
    if (value.length > 45){
      return value.substring(0,45)+ ' ...'
    }else{
      return value
    }
  }

  handleCancel(): void{
    this.isvisible = false
  }



}
