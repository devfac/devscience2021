import { NgModule } from '@angular/core';
import { AuthComponent } from './auth.component';
import { LoginComponent } from './login/login.component';
import { SharedModule } from '@app/shared/modules/shared.module';
import { AuthRoutingModule } from './auth-routing.module';
import { ChangedPasswordComponent } from './changed-password/changed-password.component';
// import { ForgotPasswordComponent } from './password/forgot-password/forgot-password.component';
// import { ResetPasswordComponent } from './password/reset-password/reset-password.component';

@NgModule({
  declarations: [
    AuthComponent,
    LoginComponent,
    ChangedPasswordComponent,
    // ForgotPasswordComponent,
    // ResetPasswordComponent,
  ],
  imports: [
    SharedModule,
    AuthRoutingModule,
  ]
})
export class AuthModule { }
