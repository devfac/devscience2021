import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { globalConfig } from '@app/configs/global.config';
import { TranslationService } from '@app/services/translation/translation.service';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.less']
})
export class AdminComponent implements OnInit {
  drawerVisible = false;
  drawerBodyStyle = {
    "padding": 0,
  }
  translate: TranslateService;
  user!: { firstName: string; lastName: string; };
  config!: {
    appLogo: string,
    appTitle: string,
    appURL: string;
    footerCopyright: string;
  }

  constructor(public translation: TranslationService, public router: Router,) {
    this.translate = this.translation.translate;
  }
 
  ngOnInit() {

    console.log("get socket")

    this.config = {
      appLogo: globalConfig.appLogo,
      appTitle: globalConfig.appTitle,
      appURL: globalConfig.appURL,
      footerCopyright: globalConfig.footerCopyright
    }
    this.user = { firstName: '', lastName: '' };
    
  }

  openDrawer(): void {
    this.drawerVisible = true;
  }

  closeDrawer(): void {
    this.drawerVisible = false;
  }
}
