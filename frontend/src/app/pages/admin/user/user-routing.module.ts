import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DetailsNoteComponent } from '../home/details-note/details-note.component';
import { NoteComponent } from '../home/note/note.component';
import { InscriptionAddComponent } from './inscription-add/inscription-add.component';
import { InscriptionComponent } from './inscription/inscription.component';
import { ReInscriptionAddComponent } from './re-inscription-add/re-inscription-add.component';
import { ReInscriptionComponent } from './re-inscription/re-inscription.component';
import { SelectionAddComponent } from './selection-add/selection-add.component';
import { SelectionComponent } from './selection/selection.component';
import { UserComponent } from './user.component';

const routes: Routes = [{ path: '',
component: UserComponent,
children: [
 {
   path: '', pathMatch: 'full',
   redirectTo: '/user/reinscription',
 },
 {
  path: 'selection',
  component: SelectionComponent,
  data: { breadcrumb: 'admin.user.selection.title' },
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
{
  path: 'selection_add',
  component: SelectionAddComponent,
  data: { breadcrumb: 'admin.user.selection.title' },
},
{
  path: 'inscription_add',
  component: InscriptionAddComponent,
  data: { breadcrumb: 'admin.user.inscription.title' },
},
{
  path: 'note',
  component: NoteComponent,
  data: { breadcrumb: 'admin.home.note.title' },
},
{
  path: 'note-details',
  component: DetailsNoteComponent,
  data: { breadcrumb: 'admin.details.note.title' },
},
]
},
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }
