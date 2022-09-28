import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { AuthService } from '../services/auth/auth.service';
import { NzMessageService } from 'ng-zorro-antd/message';
import { TranslateService } from '@ngx-translate/core';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(
    private authService: AuthService,
    private message: NzMessageService,
    private translate: TranslateService
  ) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError((err) => {
        if ([401, 403].includes(err.status) && this.authService.userValue) {
          // auto logout if 401 or 403 response returned from api
          this.authService.logout();
        }

        const error = err.error?.message || err.statusText;
        this.translate.get('server_error').subscribe((text_error) => {
          this.message.error(err.error.detail);
          console.error(err.error);
        });
        return throwError(error);
      })
    );
  }
}

