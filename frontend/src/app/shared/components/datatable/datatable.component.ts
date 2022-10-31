import { Component, EventEmitter, Input, Output } from '@angular/core';
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
  @Input() editCache: { [key: string]: { edit: boolean; data: any } } = {};
  @Input() dataStocks: any[] = [];
  @Input() width: number = 800;
  @Input() idSelector: string = 'id';
  @Input() loading: boolean = false;
  @Input() total = 0;
  @Input() pageSize = 10;
  @Input() pageIndex = 1;
  @Input() classNames?: string;
  @Input() classExpand?: string;
  @Input()
  fetchDataFn!: (params?: QueryParams) => Observable<any>;
  @Input() isSelectable: boolean = false;
  @Input() showPagination: boolean = true;
  @Input() selectedId: number | null = null;
  @Output() startEdit = new EventEmitter<void>();
  @Output() canceltEdit = new EventEmitter<void>();
  @Output() cancelStocktEdit = new EventEmitter<{ id_stock: number; id_product: number }>();
  @Output() saveEdit = new EventEmitter<{
    id_product: number;
    id: number;
    halfPalletQty: number;
    standardPalletQty: number;
    sellingPricePerUnit: number;
  }>();
  @Output() saveStockEdit = new EventEmitter<{
    id: number;
    productionTime: number;
    departurePortId: number;
    isMainStock: boolean;
    stock: number;
  }>();
  @Output() selectionChange = new EventEmitter<number | null>();
  @Output() queryParamsChange = new EventEmitter<any>();
  TableHeaderType = TableHeaderType;

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

  cancEdit(id: any): void {
    this.canceltEdit.emit(id);
  }

  cancelStocEdit(id_stock: number, id_product: any): void {
    this.cancelStocktEdit.emit({ id_stock, id_product });
  }

  savedEdit(row: any): void {
    this.saveEdit.emit({
      id_product: row.id,
      id: row.productPricingId,
      halfPalletQty: row.halfPalletQty,
      standardPalletQty: row.standardPalletQty,
      sellingPricePerUnit: row.sellingPricePerUnit,
    });
  }

  savedStockEdit(row: any): void {
    console.log(row);
    this.saveStockEdit.emit({
      id: row.id,
      isMainStock: row.isMainStock,
      departurePortId: row.departurePortId,
      stock: row.stock,
      productionTime: row.productionTime,
    });
  }
}
