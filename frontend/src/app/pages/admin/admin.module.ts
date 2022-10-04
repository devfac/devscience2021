import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/modules/shared.module';
import { BreadcrumbModule } from 'xng-breadcrumb';
import { AdminRoutingModule } from './admin-routing.module';
import { AdminComponent } from './admin.component';
import { MenuComponent } from '@app/components/menu/menu.component';
import { ProfilDropdownComponent } from '@app/components/profil-dropdown/profil-dropdown.component';
import { LanguageSelectComponent } from '@app/components/select/language-select/language-select.component';
import { UploadComponent } from './upload/upload.component';
import { UserComponent } from './user/user.component';

@NgModule({
  declarations: [
    MenuComponent,
    LanguageSelectComponent,
    ProfilDropdownComponent,
    AdminComponent,
    UploadComponent,
    UserComponent,
  ],
  imports: [
    SharedModule,
    BreadcrumbModule,
    AdminRoutingModule,
  ],
  bootstrap: [
    AdminComponent
  ]
})
export class AdminModule { }
