import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { QueryParams } from '@app/models/query';
import { TableHeader, TableHeaderType } from '@app/models/table';
import { Observable } from 'rxjs';
import { Subscription } from 'rxjs';
@Component({
  selector: 'app-datatable',
  templateUrl: './datatable.component.html',
  styleUrls: ['./datatable.component.less'],
})
export class DatatableComponent {
  @Input() tableId: string = 'Datatable';
  @Input() headers: TableHeader[] = [];
  @Input() headerSpan: TableHeader[] = [];
  @Input() headerData: TableHeader[] = [];
  @Input() childrenDataHeader: TableHeader[] = [];
  @Input() childrenDataSpan: TableHeader[] = [];
  @Input() data: any[] = [];
  @Input() portList: any[] = [];
  @Input() editCache: { [key: string]: { edit: boolean; data: any} } = {};
  @Input() dataStocks: any[] = [];
  @Input() width: number = 800;
  @Input() idSelector: string = 'id';
  @Input() loading: boolean = false;
  @Input() total = 0;
  @Input() pageSize = 10;
  @Input() pageIndex = 1;
  @Input() classNames?: string;
  @Input() message: string = ""
  @Input() classExpand?: string;
  @Input() fetchDataFn!: (params?: QueryParams) => Observable<any>;
  @Input() isSelectable: boolean = false;
  @Input() showPagination: boolean = true;
  @Input() selectedId: number | null = null;
  @Output() startEdit = new EventEmitter<void>();
  @Output() addStock = new EventEmitter<void>();
  @Output() canceltEdit = new EventEmitter<void>();
  @Output() search = new EventEmitter<void>();
  @Output() viewNote = new EventEmitter<void>();
  @Output() saveEdit = new EventEmitter<any>();
  @Output() selectionChange = new EventEmitter<number | null>();
  @Output() queryParamsChange = new EventEmitter<any>();
  TableHeaderType = TableHeaderType;

  isAdded: boolean = true;

  constructor() {
  }

  trackByIdSelector(_: number, item: any): string {
    return item[this.idSelector];
  }

  getValue(row: any, selector: string) {
    const selectors = selector.split('.');
    return selectors.reduce((a, prop) => a[prop], row);
  }

  onItemChecked(id: number, checked: boolean): void {
    if (checked) {
      this.selectedId = id;
    } else {
      this.selectedId = null;
    }
    this.selectionChange.emit(this.selectedId);
  }

  onEdit(id: any): void {
    this.startEdit.emit(id);
  }

  onStock(id: any): void {
    console.log('kjaf kaugsfakg agsf', id);
    this.addStock.emit(id);
    this.isAdded = false;
  }

  cancEdit(id: any): void {
    this.canceltEdit.emit(id);
  }

  savedEdit(row: any): void {
    this.saveEdit.emit(row);
  }

  onView(num_carte: any){
    this.viewNote.emit(num_carte)
  }

}
