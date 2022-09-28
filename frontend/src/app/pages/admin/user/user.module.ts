import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/modules/shared.module';

import { UserRoutingModule } from './user-routing.module';
import { InscriptionComponent } from './inscription/inscription.component';
import { ReInscriptionComponent } from './re-inscription/re-inscription.component';
import { ReInscriptionAddComponent } from './re-inscription-add/re-inscription-add.component';


@NgModule({
  declarations: [
    InscriptionComponent,
    ReInscriptionComponent,
    ReInscriptionAddComponent
  ],
  imports: [
    SharedModule,
    UserRoutingModule
  ]
})
export class UserModule { }
