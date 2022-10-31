import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/modules/shared.module';

import { UserRoutingModule } from './user-routing.module';
import { InscriptionComponent } from './inscription/inscription.component';
import { ReInscriptionComponent } from './re-inscription/re-inscription.component';
import { ReInscriptionAddComponent } from './re-inscription/re-inscription-add/re-inscription-add.component';
import { SelectionComponent } from './selection/selection.component';
import { SelectionAddComponent } from './selection/selection-add/selection-add.component';
import { InscriptionAddComponent } from './inscription/inscription-add/inscription-add.component';


@NgModule({
  declarations: [
    InscriptionComponent,
    ReInscriptionComponent,
    ReInscriptionAddComponent,
    SelectionComponent,
    SelectionAddComponent,
    InscriptionAddComponent
  ],
  imports: [
    SharedModule,
    UserRoutingModule
  ]
})
export class UserModule { }
