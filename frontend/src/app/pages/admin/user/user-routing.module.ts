import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InscriptionComponent } from './inscription/inscription.component';
import { ReInscriptionAddComponent } from './re-inscription-add/re-inscription-add.component';
import { ReInscriptionComponent } from './re-inscription/re-inscription.component';
import { UserComponent } from './user.component';

const routes: Routes = [{ path: '',
component: UserComponent,
children: [
 {
   path: '', pathMatch: 'full',
   redirectTo: '/user/inscription',
 },
 {
   path: 'inscription',
   component: InscriptionComponent,
   data: { breadcrumb: 'admin.user.inscription.title' },
 },
 {
  path: 'reinscription',
  component: ReInscriptionComponent,
  data: { breadcrumb: 'admin.user.reinscription.title' },
},
{
  path: 'reinscription_add',
  component: ReInscriptionAddComponent,
  data: { breadcrumb: 'admin.user.reinscription.title' },
},
]
},
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }
