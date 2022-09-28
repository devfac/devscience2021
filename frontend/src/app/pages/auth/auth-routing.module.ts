import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthComponent } from './auth.component';
import { LoginComponent } from './login/login.component';
import { ChangedPasswordComponent } from './changed-password/changed-password.component';
const routes: Routes = [
  {
    path: '',
    component: AuthComponent,
    children: [
      {
        path: '', pathMatch: 'full',
        redirectTo: '/auth/login'
      },
      {
        path: 'login',
        component: LoginComponent,
      },
      {
        path: 'password',
        children: [
          {
            path: '', pathMatch: 'full',
            redirectTo: '/auth/login'
          },
          {
            path: 'changed',
            component: ChangedPasswordComponent,
          },
        ]
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AuthRoutingModule { }
