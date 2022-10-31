import {
  AfterContentInit,
  Component,
  EventEmitter,
  Input,
  OnInit,
  Output,
  TemplateRef,
  ViewChild,
} from '@angular/core';
import { NzMessageService } from 'ng-zorro-antd/message';
import { NzTableQueryParams } from 'ng-zorro-antd/table';
import { Observable } from 'rxjs';
import { first } from 'rxjs/operators';
import * as _ from 'lodash';
import { Location } from '@angular/common';
import { QueryParams } from '@app/models/query';
import { TableHeader, TableActions, TableHeaderType } from '@app/models/table';

@Component({
  selector: 'app-datatable-crud',
  templateUrl: './datatable-crud.component.html',
  styleUrls: ['./datatable-crud.component.less'],
})
export class DatatableCrudComponent implements OnInit, AfterContentInit {
  @Input() tableId: string = 'Datatable';
  @Input() headers: TableHeader[] = [];
  @Input() headerSpan: TableHeader[] = [];
  @Input() headerData: TableHeader[] = [];
  @Input() childrenDataHeader: TableHeader[] = [];
  @Input() childrenDataSpan: TableHeader[] = [];
  @Input()
  width!: number;
  @Input() title: string = '';
  @Input() isSelectable: boolean = false;
  @Input() selectedId: number | null = null;
  @Input() searchTemplate?: TemplateRef<any>;
  @Input() showPagination: boolean = true;
  @Input() classNames?: string;
  @Input() classExpand?: string;
  @Input() canBack: boolean = false;
  @Input() actions: TableActions = {
    add: false,
    edit: false,
    delete: false,
    detail: false,
    restore: false,
  };
  @Input() isDeletedRow: Function = () => false;
  @Input()
  fetchDataFn!: (params?: QueryParams) => Observable<any>;
  @Input() anotherAction: string = '';
  @Output() add = new EventEmitter<void>();
  @Output() edit = new EventEmitter<any>();
  @Output() delete = new EventEmitter<any>();
  @Output() detail = new EventEmitter<any>();
  @Output() restore = new EventEmitter<any>();
  @Output() selectionChange = new EventEmitter<number | null>();
  @ViewChild('actionsTemplate', { static: true })
  actionsTemplate!: TemplateRef<any>;
  data: any[] = [];
  new_data: any[] = [];
  loading: boolean = false;
  total = 0;
  pageSize = 10;
  pageIndex = 1;
  sortField: string | null = null;
  sortOrder: string | null = null;
  where: any | null = null;
  searchOption: string | null = null;

  constructor(private nzMessage: NzMessageService, private location: Location) {}

  ngOnInit(): void {
    this.fetchData();
  }

  ngAfterContentInit(): void {
    setTimeout(() => {
      if (this.getActionsNumber() > 0) {
        const width = Math.max(120, this.getActionsNumber() * 45);
        this.headers = [
          ...this.headers,
          {
            title: 'Action',
            selector: 'action',
            type: TableHeaderType.ACTION,
            width: `${width}px`,
            style: { 'text-align': 'center' },
            template: this.actionsTemplate,
            isSortable: false,
          },
        ];
      }
    }, 0);
  }

  editCache: { [key: string]: { edit: boolean; data: any } } = {};
  listOfData: any[] = [];

  startEdit(id: any): void {
    this.editCache[id].edit = true;
  }

  cancelEdit(id: any, listOfData: any[]): void {
    const index = this.listOfData.findIndex((item) => item.id === id);
    Object.assign(listOfData[index], this.listOfData[index]);
    this.editCache[id] = {
      data: { ...this.listOfData[index] },
      edit: false,
    };
  }

  cancelStockEdit(id: any, listOfData: any[], data: any[]): void {
    console.log(this.listOfData);
    console.log(id.id_stock);
    const index_data = this.data.findIndex((item) => item.id === id.id_product);
    let stocks: any[] = this.data[index_data].stocks;
    const index_stocks = stocks.findIndex((item) => item.id === id.id_stock);
    const index = this.listOfData.findIndex((item) => item[0].id === id.id_stock);

    Object.assign(data[index_data].stocks[index_stocks], this.listOfData[index]);
    this.editCache[id.id_stock] = {
      data: { ...this.listOfData[index] },
      edit: false,
    };
  }

  saveEdit(row: any, listOfData: any[]): void {
    console.log(row);
    const index = this.listOfData.findIndex((item) => item.id === row.id_product);
    this.edit.emit(row);
    //Object.assign(this.listOfData[index], listOfData[index]);
    this.editCache[row.id_product].edit = false;
  }

  saveStockEdit(row: any, listOfData: any[]): void {
    console.log(row);
    const index = this.listOfData.findIndex((item) => item.id === row.id);
    this.edit.emit(row);
    // Object.assign(this.listOfData[index], listOfData[index]);
    this.editCache[row.id].edit = false;
  }

  updateEditCache(): void {
    this.listOfData.forEach((item) => {
      this.editCache[item.id] = {
        edit: false,
        data: { ...item },
      };
    });
  }

  public fetchData(
    params?: QueryParams,
    debounceTime = 0
  ) {
    let _params: QueryParams;
    if (this.fetchDataFn) {
      _.debounce(() => {
        if (!params) {
          _params = {
            pageIndex: this.pageIndex,
            pageSize: this.pageSize,
            sortField: this.sortField,
            sortOrder: this.sortOrder,
          };
        } else {
          _params = { ...params };
        }

        this.loading = true;
        console.log('paramse', _params)
        this.fetchDataFn(_params)
          ?.pipe(first())
          .subscribe({
            next: (result) => {
              console.log('result',result)
              this.loading = false;
              this.new_data = [];
              this.listOfData = [];
              /*
              if (this.childrenDataHeader.length > 0) {
                for (let i = 0; i < result; i++) {
                  this.new_data.push({ ...result.data[i], expand: false });
                  this.listOfData.push({ ...result.data[i].stocks });

                  for (let j = 0; j < result.data[i].stocks.length; j++) {
                    this.editCache[result.data[i].stocks[j].id] = {
                      edit: false,
                      data: { ...result.data[i].stocks },
                    };
                  }
                }
              } else {
                for (let i = 0; i < result.data.length; i++) {
                  this.new_data.push({ ...result.data[i], expand: false });
                  this.listOfData.push({ ...result.data[i] });
                  this.editCache[result.data[i].id] = {
                    edit: false,
                    data: { ...result.data[i] },
                  };
                }
              }
              */
              this.total = result?.meta?.itemCount || 0;
              this.data = result;
            },
            error: (err) => {
              console.error(err);
              this.nzMessage.error('Fetching error');
              this.loading = false;
            },
          });
      }, debounceTime)();
    }
  }

  onQueryParamsChange(params: NzTableQueryParams): void {
    const { pageSize, pageIndex, sort } = params;
    const currentSort = sort.find((item) => item.value !== null);
    const sortField = (currentSort && currentSort.key) || null;
    const sortOrder = (currentSort && currentSort.value) || null;
    this.pageIndex = pageIndex;
    this.pageSize = pageSize;
    this.sortField = sortField;
    this.sortOrder = sortOrder;
    this.fetchData({
      pageIndex,
      pageSize,
      sortField,
      sortOrder,
    });
  }

  onSelectionChange(id: number | null) {
    this.selectionChange.emit(id);
  }

  getActionsNumber() {
    return +(this.actions.edit || 0) + +(this.actions.delete || 0) + +(this.actions.detail || 0);
  }

  onAdd() {
    this.add.emit();
  }

  onRestore(row: any) {
    this.restore.emit(row);
  }

  onEdit(row: any) {
    this.edit.emit(row);
  }

  saveEditData(row: any) {
    this.edit.emit(row);
  }

  onDelete(row: any) {
    this.delete.emit(row);
  }

  onDetail(row: any) {
    this.detail.emit(row);
  }

  back(): void {
    this.location.back();
  }
}
