import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@environments/environment';
import { AuthService } from '@app/services/auth/auth.service';

const BASE_URL = environment.authApiURL;

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  constructor(private authServcice: AuthService) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // add auth header with jwt if user is logged in and request is to the api url
    const user = this.authServcice.userValue;
    const isLoggedIn = user && user.first_name;
    const isApiUrl = request.url.startsWith(BASE_URL);
    if (isLoggedIn && isApiUrl) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${user?.access_token}`
        }
      });
    }

    return next.handle(request);
  }
}
