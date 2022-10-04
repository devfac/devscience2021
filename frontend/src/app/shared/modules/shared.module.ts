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
//import { CurrencyPricePipe } from '../pipes/currency-price/currency-price.pipe';

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
   // CurrencyPricePipe,
  ],
  declarations: [
    LanguageSwitcherComponent,
    NotificationStatusDirective,
    CustomAutoFocusDirective,
    CustomBackgroundDirective,
    // CurrencyPricePipe,
  ],
})
export class SharedModule { }
