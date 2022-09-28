import { NgModule } from '@angular/core';
import { EditPasswordComponent } from './edit-password/edit-password.component';
import { ProfileComponent } from './profile.component';
import { SharedModule } from '@app/shared/modules/shared.module';
import { ProfileRoutingModule } from './profile-routing.module';
import { GeneralComponent } from './general/general.component';



@NgModule({
  declarations: [
    EditPasswordComponent,
    ProfileComponent,
    GeneralComponent,
  ],
  imports: [
    SharedModule,
    ProfileRoutingModule,
  ]
})
export class ProfileModule { }
