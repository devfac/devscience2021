import { Injectable } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

@Injectable({
  providedIn: 'root',
})
export class TranslationService {
  constructor(public translate: TranslateService) {
    const currentLanguage = localStorage.getItem('language');
    translate.addLangs(['en', 'fr']);

    if (currentLanguage) {
      translate.setDefaultLang(currentLanguage);
      translate.use(currentLanguage);
    } else {
      translate.setDefaultLang('en');
      translate.use('en');
      localStorage.setItem("language", "en");
    }
  }

  setTranslationTo(lang: string) {
    this.translate.use(lang);
    localStorage.setItem('language', lang);
  }
}
