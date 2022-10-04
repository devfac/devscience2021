import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
// import { CurrencyService } from '@app/services/currency/currency.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.less'],
})
export class HomeComponent implements OnInit {
  user!: { firstName: string; lastName: string };

  ngOnInit(): void {
    this.user = { firstName: 'John', lastName: 'Shark' };
  }

  constructor(public router: Router) { }

}
