import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { typePermission } from '@app/data/data';
import { Message } from '@app/models/chatMessage';
import { Permission } from '@app/models/permission';
import { AuthService } from '@app/services/auth/auth.service';
import { SocketService } from '@app/socket.service';
import { environment } from '@environments/environment';

const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-permission',
  templateUrl: './permission.component.html',
  styleUrls: ['./permission.component.less']
})
export class PermissionComponent implements OnInit {
  
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+window.sessionStorage.getItem('token')
  })
  form!: FormGroup;
  typePermission=typePermission
  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private socketService: SocketService,
    private authUser: AuthService,
    ) {
        this.form = this.fb.group({
      email: [null, [Validators.required]],
      time: [null, [Validators.required]],
      type: [null, [Validators.required]],
    }); }

  ngOnInit(): void {
  }
  async submitForm(){
    if (this.form.valid) {
      const data = {
        email: this.form.value.email,
        time: this.form.value.time,
        type: this.form.value.type,
        accepted: true,
      }
      await this.createPermission(data).toPromise()
      let chatMsg: Message = {message: "Permission "+this.form.value.type +" accordé, expiré dans "+this.form.value.time+"h", to: this.form.value.email}
      this.socketService.sendMessage(chatMsg )
      this.socketService.createNotification("bottomRight","Permission envoyé",this.form.value.email)

  }
}
createPermission(data: any){
  return  this.http.post<Permission>(`${BASE_URL}/permission/`,data, {headers: this.headers})
}
}
