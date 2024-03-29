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
import { otherQueryParams, QueryParams } from '@app/models/query';
import { TableHeader, TableActions, TableHeaderType } from '@app/models/table';
import { Ue } from '@app/models/ue';
import { Ec } from '@app/models/ec';
import { FormBuilder, FormGroup } from '@angular/forms';
import { TranslateService } from '@ngx-translate/core';
import { AuthService } from '@app/services/auth/auth.service';
import { NoteService } from '@app/pages/admin/home/note/note.service';
import { User } from '@app/models';

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
  @Input() matierUe: Ue[] = [];
  @Input() matierEc: Ec[] = [];
  @Input() width!: number;
  @Input() title: string = '';
  @Input() tableTitle?: string;
  @Input() session: string = '';
  @Input() portList: any[] = [];
  @Input() isSelectable: boolean = false;
  @Input() permission: boolean = true;
  @Input() permissionUser: boolean = true;
  @Input() permissionNote: boolean = false;
  @Input() isNote: boolean = false
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
    print: false,
  };
  @Input() isDeletedRow: Function = () => false;
  @Input() fetchDataFn!: (params?: QueryParams, otherParams?: otherQueryParams) => Observable<any>;
  @Input() anotherAction: string = '';
  @Output() add = new EventEmitter<void>();
  @Output() download = new EventEmitter<void>();
  @Output() edit = new EventEmitter<any>();
  @Output() delete = new EventEmitter<any>();
  @Output() detail = new EventEmitter<any>();
  @Output() compareUesup = new EventEmitter<{ue: string, value_ue: string}>();
  @Output() startSearch = new EventEmitter<any>();
  @Output() demande = new EventEmitter<any>();
  @Output() resultUeSuccess = new EventEmitter<any>();
  @Output() resultUeFaild = new EventEmitter<any>();
  @Output() resultEcSuccess = new EventEmitter<any>();
  @Output() resultEcFailed = new EventEmitter<any>();
  @Output() listRattrapage = new EventEmitter<any>();
  @Output() resultByCreditSuccess = new EventEmitter<any>();
  @Output() selectionChange = new EventEmitter<number | null>();
  @Output() search = new EventEmitter<string | null>();
  @ViewChild('actionsTemplate', { static: true }) actionsTemplate!: TemplateRef<any>;


  @Output() refresh = new EventEmitter<any>();
  @Output() listExam = new EventEmitter<any>();
  @Output() downloadResult = new EventEmitter<any>();
  @Output() deleteTable = new EventEmitter<any>();
  @Output() createTable = new EventEmitter<any>();
  @Output() insert = new EventEmitter<any>();

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
  idExpand: number = 0;
  isVisible: boolean = true
  isResult: boolean = false
  isRattrape: boolean = false
  result: string = ""
  user!: User;
  form!: FormGroup;
  listOfFilter = ["Moyenne" ,"Credit"]
  message: string = "FacSciences"
  constructor(
    private nzMessage: NzMessageService,
    private location: Location,
    private translate: TranslateService,
    private authService: AuthService,
    private noteService: NoteService,
    private fb: FormBuilder, ) {
    this.form = this.fb.group({
    matierUe: [null],
    matierEc: [null],
    meanCredit: [null],
    filter: [null],
    search:[]
    })
  }

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

  editCache: { [key: string]: { edit: boolean; data: any;} } = {};
  listOfData: any[] = [];

  async startEdit(id: any) {
    let permission = await this.noteService.getPermission(this.authService.userValue?.email, 'note').toPromise()
          if (permission){
            this.permissionNote = permission.accepted
          }

          if (permission.accepted){
            this.editCache[id].edit = true;
          }
  }

  cancelEdit(id: any, listOfData: any[]): void {
    const index = this.listOfData.findIndex((item) => item.num_carte === id);
    Object.assign(listOfData[index], this.listOfData[index]);
    this.editCache[id] = {
      data: { ...this.listOfData[index] },
      edit: false,
    };
  }
  saveEdit(row: any): void {
    this.idExpand = row.productId;
    const index = this.listOfData.findIndex((item) => item.num_carte === row.num_carte);
    this.edit.emit(row);
    //Object.assign(this.listOfData[index], listOfData[index]);
    this.editCache[row.num_carte].edit = false;
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
    params?: QueryParams | null,
    additional?: otherQueryParams,
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

        if (additional) {
          _params = { ..._params };
        }
        this.loading = true;
        this.fetchDataFn(_params, additional)
          ?.pipe(first())
          .subscribe({
            next: (result) => {
              this.loading = false;
              this.new_data = [];
              this.listOfData = [];
              //this.data = result
              if (this.childrenDataHeader?.length > 0) {
                for (let i = 0; i < result.data.length; i++) {
                  this.new_data.push({ ...result.data[i], expand: false, add: false });
                  this.listOfData.push({ ...result.data[i] });

                }
              } else {
                for (let i = 0; i < result.data.length; i++) {
                  this.new_data.push({ ...result.data[i]});
                  this.listOfData.push({ ...result.data[i] });
                  this.editCache[result.data[i].num_carte] = {
                    edit: false,
                    data: { ...result.data[i] },
                  };
                }
              }
              this.total = result?.count || 0;
              this.data = [...this.new_data];


            },
            error: (err) => {
              console.error("erroe as", err);
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

  onEdit(row: any) {
    this.edit.emit(row);
  }

  onSearch() {
    if(this.form.value.search){
      this.search.emit(this.form.value.search);
    }else{
      this.search.emit(null);
    }
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

  onDownload(){
    this.download.emit();
  }

  compareNoteSupUe(): void{
    if (this.form.value.matierUe){
      this.resultUeSuccess.emit(this.form.value.matierUe)
    }else{
      this.resultUeSuccess.emit(null)
    }
  }

  insertStudent(){
    this.insert.emit()
  }
  setVisible(){
    this.isVisible = !this.isVisible
  }
  onRefresh(){
    this.refresh.emit()
  }
  onExamList(){
    this.listExam.emit()
  }
  onDeleteTable(){
    this.deleteTable.emit()
  }

  onCreateTable(){
    this.createTable.emit()
  }
  filterSup(){
    if (this.form.value.filter){
      let value = this.form.value.meanCredit
      localStorage.setItem('lastBtn', 'sup')
        if (localStorage.getItem('filter') === 'Moyenne' ){
          const data ={
            credit:null,
            mean:"mean",
            value:value
          }
          this.resultByCreditSuccess.emit(data)
        }else{
          const data ={
            credit:"credit",
            mean:null,
            value:value
            }
        this.resultByCreditSuccess.emit(data)
        }
    }else{
      this.resultByCreditSuccess.emit(null)
    }
  }
  filterInf(){
    if (this.form.value.filter){
      let value = this.form.value.meanCredit
      localStorage.setItem('lastBtn', 'sup')
        if (localStorage.getItem('filter') === 'Moyenne' ){
          this.data = this.new_data.filter((item: any) => item['mean']  < Number(value) )
        }else{
          this.data = this.new_data.filter((item: any) => item['credit']  < Number(value) )
        }
    }else{
      this.data = this.new_data
    }
  }
  resetTableUe(){
    if (this.form.value.matierUe){
      this.result = this.form.value.matierUe
      this.isResult = true
    }else{
      this.data = this.new_data;
      this.isResult = false
    }
  }
  compareNoteInfUe(){
    if (this.form.value.matierUe){
      this.resultUeFaild.emit(this.form.value.matierUe)
    }else{
      this.resultUeFaild.emit(this.form.value.matierUe)
    }
  }
  resultat(){
    this.downloadResult.emit(this.form.value.matierUe)
  }
  resetTableEc(){
    if (this.form.value.matierEc){
      this.result = this.form.value.matierEc
      this.isRattrape = true
    }else{
      this.data = this.new_data;
      this.isRattrape = false
    }
  }
  compareNoteSupEc(){
    if (this.form.value.matierEc){
      this.resultEcSuccess.emit(this.form.value.matierEc)
    }else{
      this.resultEcSuccess.emit(null)
    }
  }
  compareNoteInfEc(){
    if (this.form.value.matierEc){
      this.resultEcFailed.emit(this.form.value.matierEc)
    }else{
      this.resultEcFailed.emit(null)
    }

  }
  rattrapageList(){
    if (this.form.value.matierEc && this.session === 'Normal'){
      const name = this.matierEc.find((item:Ec) => item.value === this.form.value.matierEc)
      const data ={valueEc:this.form.value.matierEc, valueUe:name?.value_ue}
      this.listRattrapage.emit(data)
  }else{
    this.listRattrapage.emit(null)
  }
  }
  changeFilter(){
    if (this.form.value.filter){
      localStorage.setItem('filter', this.form.value.filter)
    }else{
      localStorage.setItem('filter', '')
    }
  }
  onDemande(){
    this.demande.emit()
  }
}
