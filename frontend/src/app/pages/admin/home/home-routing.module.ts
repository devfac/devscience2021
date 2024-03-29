import { NgModule } from '@angular/core';
import { Router, RouterModule, Routes } from '@angular/router';
import { ClassroomComponent } from './classroom/classroom.component';
import { CollegeYearComponent } from './college-year/college-year.component';
import { DetailsNoteComponent } from './details-note/details-note.component';
import { DroitComponent } from './droit/droit.component';
import { EcComponent } from './ec/ec.component';
import { HomeComponent } from './home.component';
import { JourneyComponent } from './journey/journey.component';
import { MentionComponent } from './mention/mention.component';
import { NoteComponent } from './note/note.component';
import { PermissionComponent } from './permission/permission.component';
import { RoleComponent } from './role/role.component';
import { UeComponent } from './ue/ue.component';
import { UsersComponent } from './users/users.component';
import { BaccSerieComponent } from './bacc-serie/bacc-serie.component';
import { HistoricComponent } from './historic/historic.component';
import { PublicationComponent } from './publication/publication.component';

const routes: Routes = [
  { path: '',
   component: HomeComponent,
  children: [
    {
      path: '', pathMatch: 'full',
      redirectTo: '/home/users',
    },
    {
      path: 'users',
      component: UsersComponent,
      data: { breadcrumb: 'admin.home.users.title' },
    },
    {
      path: 'mention',
      component: MentionComponent,
      data: { breadcrumb: 'admin.home.mention.title' },
    },
    {
      path: 'journey',
      component: JourneyComponent,
      data: { breadcrumb: 'admin.home.journey.title' },
    },
    {
      path: 'college-year',
      component: CollegeYearComponent,
      data: { breadcrumb: 'admin.home.college_year.title' },
    },
    {
      path: 'role',
      component: RoleComponent,
      data: { breadcrumb: 'admin.home.role.title' },
    },
    {
      path: 'ue',
      component: UeComponent,
      data: { breadcrumb: 'admin.home.ue.title' },
    },
    {
      path: 'ec',
      component: EcComponent,
      data: { breadcrumb: 'admin.home.ec.title' },
    }, 
    {
      path: 'note',
      component: NoteComponent,
      data: { breadcrumb: 'admin.home.note.title' },
    },
    {
      path: 'note-details',
      component: DetailsNoteComponent,
      data: { breadcrumb: 'admin.home.details.title' },
    },
    {
      path: 'permission',
      component: PermissionComponent,
      data: { breadcrumb: 'admin.home.permission' },
    }, 
    {
      path: 'droit',
      component: DroitComponent,
      data: { breadcrumb: 'admin.home.droit.title' },
    },
    {
      path: 'classroom',
      component: ClassroomComponent,
      data: { breadcrumb: 'admin.home.classroom.title' },
    },
    {
      path: 'bacc-serie',
      component: BaccSerieComponent,
      data: { breadcrumb: 'admin.home.bacc_serie.title' },
    },
    {
      path: 'historic',
      component: HistoricComponent,
      data: { breadcrumb: 'admin.home.historic.title' },
    },
    {
      path: 'publication',
      component: PublicationComponent,
      data: { breadcrumb: 'admin.home.publication.title' },
    },
  ]
 },
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HomeRoutingModule {
}





