import { Component, OnInit } from '@angular/core';
@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.less'],
})
export class AboutComponent implements OnInit {
  user!: { firstName: string; lastName: string };

  constructor() {}

  ngOnInit(): void {
    this.user = { firstName: 'John', lastName: 'Shark' };
  }
}
