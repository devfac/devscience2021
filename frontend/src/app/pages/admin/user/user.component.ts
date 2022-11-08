import { Component, OnInit } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { Menu } from '@app/models/menu';
import { UserService } from './user.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.less']
})
export class UserComponent implements OnInit {
  menu: Menu[] = [];
  collapsible = true;
  collapsed = false;
  isSearchable = false;
  showSider: boolean = true;
  user!: { firstName: string; lastName: string };

  ngOnInit(): void {
    this.user = { firstName: 'John', lastName: 'Shark' };
  }

 
  constructor(public router: Router, public service: UserService) {

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.isSearchable = false;
        this.collapsible = true;
        if (event.url === '/product/product-list' || event.url === '/product') {
          this.collapsed = false;
          this.isSearchable = true;
          this.collapsible = false;
        }
      }
    });
    this.menu = this.service.menu;
    this.showSider = this.service.showSider;
    this.service.menu$.subscribe((menu) => {
      this.menu = [...menu];
    });
    this.service.showSider$.subscribe((showSider) => {
      this.showSider = showSider;
    });
   }

   checkSelected(item: any) {
    if (item.selected) {
      const path = item.selected;
      let regex: RegExp;
      if (typeof path === 'string') {
        regex = new RegExp(`^${path}` || '');
      } else {
        regex = path;
      }
      return (this.router.routerState.snapshot.url.match(regex)?.length || []) > 0;
    } else {
      if (item.fragment) {
        const _fragment = this.router.routerState.root.snapshot.fragment;
        if (_fragment === null) {
          return item.fragment === 'product-information';
        }
        return _fragment === item.fragment;
      }
      return false;
    }
  }
}
