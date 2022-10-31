import { AfterContentInit, Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { TableHeader } from '@app/models/table';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { AboutService } from './about.service';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.less'],
})
export class AboutComponent implements OnInit, AfterContentInit {
  @ViewChild(DatatableCrudComponent)
  datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];
  constructor(
    public service: AboutService,){}
  ngOnInit(): void {
    this.fetchData = this.fetchData.bind(this)
  }

  fetchData(){
    return this.service.getDataObservable()
  }

  ngAfterContentInit(): void {
    this.headers = [
      {
        title: 'Titre',
        selector: 'title',
        isSortable: true,
      },
      {
        title: 'Code',
        selector: 'code',
        isSortable: true,
      },
    ];
  }

}