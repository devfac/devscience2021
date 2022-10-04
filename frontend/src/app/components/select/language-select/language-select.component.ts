import { Component } from '@angular/core';
import { TranslationService } from '@app/services/translation/translation.service';

@Component({
  selector: 'app-language-select',
  templateUrl: './language-select.component.html',
  styleUrls: ['../select.component.less']
})
export class LanguageSelectComponent {

  constructor(public translation: TranslationService) { }

}
