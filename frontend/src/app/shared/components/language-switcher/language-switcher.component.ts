import { Component } from '@angular/core';
import { TranslationService } from '@app/services/translation/translation.service';

@Component({
  selector: 'app-language-switcher',
  templateUrl: './language-switcher.component.html',
  styleUrls: ['./language-switcher.component.less'],
})
export class LanguageSwitcherComponent {

  constructor(public translation: TranslationService) { }

}
