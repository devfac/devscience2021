import { NgModule } from '@angular/core';
import { HomeRoutingModule } from './home-routing.module';
import { HomeComponent } from './home.component';
import { SharedModule } from '@app/shared/modules/shared.module';
import { UsersComponent } from './users/users.component';
import { MentionComponent } from './mention/mention.component';
import { JourneyComponent } from './journey/journey.component';
import { CollegeYearComponent } from './college-year/college-year.component';
import { RoleComponent } from './role/role.component';
import { UeComponent } from './ue/ue.component';
import { EcComponent } from './ec/ec.component';
import { NoteComponent } from './note/note.component';
import { DetailsNoteComponent } from './details-note/details-note.component';
import { PermissionComponent } from './permission/permission.component';
import { DroitComponent } from './droit/droit.component';
import { ClassroomComponent } from './classroom/classroom.component';
import { BaccSerieComponent } from './bacc-serie/bacc-serie.component';
import { HistoricComponent } from './historic/historic.component';
import { PublicationComponent } from './publication/publication.component';

@NgModule({
  declarations: [HomeComponent, UsersComponent, MentionComponent, JourneyComponent, CollegeYearComponent, RoleComponent, UeComponent, EcComponent, NoteComponent, DetailsNoteComponent, PermissionComponent, DroitComponent, ClassroomComponent, BaccSerieComponent, HistoricComponent, PublicationComponent],
  imports: [SharedModule, HomeRoutingModule],
})
export class HomeModule { }