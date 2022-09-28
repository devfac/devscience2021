import { Component} from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '@app/services/auth/auth.service';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.less']
})
export class AuthComponent {

  constructor(private router: Router, private authService: AuthService) {
    if (this.authService.userValue) {
      // redirect to home if already logged in
      this.router.navigate(['/']);
    }
  }

}
