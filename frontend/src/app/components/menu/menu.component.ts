import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';
import { NzMenuModeType } from 'ng-zorro-antd/menu'

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.less']
})
export class MenuComponent {
  @Input() mode: NzMenuModeType = 'horizontal';
  @Output() closeDrawer = new EventEmitter<void>();

  constructor(public router: Router) { }
}
