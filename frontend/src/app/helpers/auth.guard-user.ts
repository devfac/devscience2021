import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../services/auth/auth.service';


@Injectable({ providedIn: 'root' })
export class AuthGuardUser implements CanActivate {
  constructor(
    private router: Router,
    private authService: AuthService
  ) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    const user = JSON.parse( window.sessionStorage.getItem('user') || 'null')
    if (user?.is_superuser) {
      // authorised so return true
      return true;
    }
    // not logged in so redirect to login page with the return url
    this.router.navigate(['/user'], { queryParams: { returnUrl: state.url } });
    return false;
  }
}
