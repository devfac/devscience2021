import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuardSuperUser } from '@app/helpers/auth.guard-superuser';
import { AuthGuardUser } from '@app/helpers/auth.guard-user';
import { AdminComponent } from './admin.component';

const routes: Routes = [
  {
    path: '',
    component: AdminComponent,
    children: [
      {
        path: '', pathMatch: 'full',
        redirectTo: '/home/users'
      },
      {
        path: 'home',
        loadChildren: () => import('./home/home.module').then((m) => m.HomeModule),
        data: { breadcrumb: 'home' },
        canActivate: [AuthGuardUser],
      },
      {
        path: 'about',
        loadChildren: () => import('./about/about.module').then((m) => m.AboutModule),
        data: { breadcrumb: 'about' },
      },
      {
        path: 'profile',
        loadChildren: () => import('./profile/profile.module').then((m) => m.ProfileModule),
        data: { breadcrumb: 'profile'}
      },
      {
        path: 'user',
        loadChildren: () => import('./user/user.module').then((m) => m.UserModule),
        data: { breadcrumb: 'upload'},
        canActivate: [AuthGuardSuperUser],
      },
      {
        path: 'upload',
        loadChildren: () => import('./upload/upload.module').then((m) => m.UploadModule),
        data: { breadcrumb: 'upload'}
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AdminRoutingModule { }
