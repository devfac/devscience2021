import { Component } from '@angular/core';
import { User } from '@app/models';
import { AuthService } from '@app/services/auth/auth.service';

@Component({
  selector: 'app-profil-dropdown',
  templateUrl: './profil-dropdown.component.html',
  styleUrls: ['./profil-dropdown.component.less']
})
export class ProfilDropdownComponent {
  user: User | null = null;

  constructor(private authService: AuthService) {
    this.authService.user.subscribe(_user => {
      this.user = _user;
    });
  }

  logout() {
    this.authService.logout();
  }

}
