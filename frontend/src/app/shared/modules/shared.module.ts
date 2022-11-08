import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { TranslateModule } from "@ngx-translate/core";
import { IconsProviderModule } from "@app/providers/icons-provider.module";
import { NgZorroModule } from "./ng-zorro.module";
import { LanguageSwitcherComponent } from '../components/language-switcher/language-switcher.component';
import { ScrollingModule } from "@angular/cdk/scrolling";
import { NotificationStatusDirective } from "../directives/notification-status/notification-status.directive";
import { CustomAutoFocusDirective } from '../directives/custom-auto-focus/custom-auto-focus.directive';
import { CustomBackgroundDirective } from '../directives/custom-background/custom-background.directive';
import { DatatableComponent } from '../components/datatable/datatable.component';
import { DatatableCrudComponent } from '../components/datatable-crud/datatable-crud.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    NgZorroModule,
    TranslateModule,
    IconsProviderModule,
    ScrollingModule,
  ],
  exports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    NgZorroModule,
    TranslateModule,
    IconsProviderModule,
    LanguageSwitcherComponent,
    NotificationStatusDirective,
    CustomBackgroundDirective,
    CustomAutoFocusDirective,
    ScrollingModule,
    DatatableComponent,
    DatatableCrudComponent,
   // CurrencyPricePipe,
  ],
  declarations: [
    LanguageSwitcherComponent,
    NotificationStatusDirective,
    CustomAutoFocusDirective,
    CustomBackgroundDirective,
    DatatableComponent,
    DatatableCrudComponent,
    // CurrencyPricePipe,
  ],
})
export class SharedModule { }
