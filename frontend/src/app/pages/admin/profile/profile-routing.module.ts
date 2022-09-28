import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EditPasswordComponent } from './edit-password/edit-password.component';
import { GeneralComponent } from './general/general.component';
import { ProfileComponent } from './profile.component';

const routes: Routes = [
  {
    path: '',
    component: ProfileComponent,
    children: [
      {
        path: '', pathMatch: 'full',
        redirectTo: '/profile/general',
      },
      {
        path: 'general',
        component: GeneralComponent,
        data: { breadcrumb: 'admin.profile.general.title' },
      },
      {
        path: 'edit-password',
        component: EditPasswordComponent,
        data: { breadcrumb: 'admin.profile.edit_password.title' },
      }
    ]
  },
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProfileRoutingModule { }





