import { Component, OnInit } from '@angular/core';
import { User } from '@app/models';
import { AuthService } from '@app/services/auth/auth.service';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-general',
  templateUrl: './general.component.html',
  styleUrls: ['./general.component.less']
})
export class GeneralComponent {
  user: User | null = null;

  constructor(private authService: AuthService, public translate: TranslateService) {
    this.authService.user.subscribe(_user => {
      this.user = _user;
    });
  }
}
