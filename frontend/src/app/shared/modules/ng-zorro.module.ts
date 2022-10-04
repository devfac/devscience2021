import { NgModule } from "@angular/core";
import { NzLayoutModule } from "ng-zorro-antd/layout";
import { NzMenuModule } from "ng-zorro-antd/menu";
import { NzBreadCrumbModule } from "ng-zorro-antd/breadcrumb";
import { NzDrawerModule } from "ng-zorro-antd/drawer";
import { NzSelectModule } from "ng-zorro-antd/select";
import { NzGridModule } from "ng-zorro-antd/grid";
import { NzDropDownModule } from "ng-zorro-antd/dropdown";
import { NzButtonModule } from "ng-zorro-antd/button";
import { NzInputModule } from "ng-zorro-antd/input";
import { NzFormModule } from "ng-zorro-antd/form"
import { NzCheckboxModule } from "ng-zorro-antd/checkbox";
import { NzNotificationModule } from "ng-zorro-antd/notification";
import { NzModalModule} from "ng-zorro-antd/modal";
import { NzBadgeModule } from "ng-zorro-antd/badge";
import { NzTypographyModule } from "ng-zorro-antd/typography";
import { NzPopconfirmModule } from "ng-zorro-antd/popconfirm";
import { NzAlertModule } from "ng-zorro-antd/alert";
import { NzMessageModule } from "ng-zorro-antd/message";
import { NzSpinModule } from "ng-zorro-antd/spin";
import { NzDescriptionsModule } from "ng-zorro-antd/descriptions";
import { NzTabsModule } from "ng-zorro-antd/tabs";
import { NzTableModule} from "ng-zorro-antd/table";
import { NzDividerModule } from "ng-zorro-antd/divider"
import { NzSwitchModule } from "ng-zorro-antd/switch"
import { NzDatePickerModule} from "ng-zorro-antd/date-picker"

@NgModule({
  exports: [
    NzLayoutModule,
    NzMenuModule,
    NzDrawerModule,
    NzSelectModule,
    NzGridModule,
    NzBreadCrumbModule,
    NzDropDownModule,
    NzButtonModule,
    NzInputModule,
    NzFormModule,
    NzCheckboxModule,
    NzNotificationModule,
    NzModalModule,
    NzBadgeModule,
    NzTypographyModule,
    NzPopconfirmModule,
    NzAlertModule,
    NzMessageModule,
    NzSpinModule,
    NzDescriptionsModule,
    NzTabsModule,
    NzTableModule,
    NzDividerModule,
    NzSwitchModule,
    NzDatePickerModule
  ],
})
export class NgZorroModule { }
