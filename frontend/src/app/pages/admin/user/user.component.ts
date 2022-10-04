import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.less']
})
export class UserComponent implements OnInit {
  user!: { firstName: string; lastName: string };

  ngOnInit(): void {
    this.user = { firstName: 'John', lastName: 'Shark' };
  }

  constructor(public router: Router) { }

}
