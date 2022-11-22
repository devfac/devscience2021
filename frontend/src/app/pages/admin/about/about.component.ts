import { AfterViewInit, Component, OnDestroy, OnInit } from '@angular/core';
import { environment } from '@environments/environment';
import { SocketService } from '@app/socket.service';
import { ChatMessage } from '@app/models/chatMessage';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import {webSocket, WebSocketSubject} from "rxjs/webSocket"
import { catchError, switchAll } from 'rxjs/operators';

const socketUrl = environment.socketApiURL

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.less'],
})
export class AboutComponent implements OnInit, OnDestroy {
  form!: FormGroup;

  constructor(
      public chatService: SocketService,
     private fb: FormBuilder
  ) {
    this.form = this.fb.group({
      title: [null, [Validators.required]],
      mean: [null, [Validators.required]],
    });
  }
  ngOnDestroy(): void {
    this.chatService.closeConnection()
  }
  sendMessage(): void{
    
  }
  async ngAfterViewInit() {
  }

  async ngOnInit() {
  }
  submitted = false

  submitForm(){
    this.submitted = true
  }

}
