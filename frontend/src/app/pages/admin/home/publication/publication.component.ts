import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { typePublication } from '@app/data/data';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { QueryParams } from '@app/models/query';
import { TableHeader } from '@app/models/table';
import { Ue } from '@app/models/ue';
import { parseQueryParams } from '@app/shared/utils';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { ClassroomService } from '../classroom/classroom.service';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { PublicationService } from './publication.service';
import { Publication } from '@app/models/publication';
import { HttpClient } from '@angular/common/http';

const BASE_URL = environment.onlineAPI;


@Component({
  selector: 'app-publication',
  templateUrl: './publication.component.html',
  styleUrls: ['./publication.component.less']
})
export class PublicationComponent implements OnInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];

  user = localStorage.getItem('user')
  allYears: CollegeYear[] = []
  allJourney: Journey[] = []
  allMention: Mention[] = []
  allUe: Ue[] = []
  listOfSemester = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  semesterTitles: any[] = []
  confirmModal?: NzModalRef;
  form!: FormGroup;
  form_years!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  uuid= "";
  isVisible: boolean= false
  disabled: boolean = false
  typePublicationn = typePublication;
  actualYear: string | null = ""
  titles: any[] = []

  msg!: string ;
  url: string | ArrayBuffer | null = "";
  uploadedFile: any = null;

  actions = {
    add: true,
    edit: true,
    delete: true,
    detail: false,
  };
  
  isInit: boolean = false
  constructor(private http: HttpClient,
    private modal: NzModalService, 
    private fb: FormBuilder,
    private service: PublicationService,
    ) { 
      this.form = this.fb.group({
        title: [null, [Validators.required]],
        type: [null, [Validators.required]],
        description: [null, [Validators.required]],
        expiration: [null, [Validators.required]],
        auteur: [null],
      });}

  async ngAfterContentInit() {
    this.headers = [
    {
      title: 'Title',
      selector: 'title',
      isSortable: true,
    },
    {
      title: 'type',
      selector: 'type',
      isSortable: true,
    },
    {
      title: 'Auteur',
      selector: 'auteur',
      isSortable: false,
    },
    {
      title: 'Date Expiration',
      selector: 'expiration_date',
      isSortable: true,
    }
  ];

  }

  async ngOnInit(){
    this.fetchData = this.fetchData.bind(this)
  }
  fetchData(params?: QueryParams){
    return this.service.getDataObservable(parseQueryParams(params))
  }
  testStorage(key: string, value: string){
    if(localStorage.getItem(key)){
      this.form.get(key)?.setValue(localStorage.getItem(key))
    }else{
      localStorage.setItem(key, value)
      this.form.get(key)?.setValue(localStorage.getItem(key))
    }
  }

  showConfirm(name: string, uuid: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: async () => {
        await this.service.deletData(uuid)
        this.datatable.fetchData()
      }
    })
  }

  onDelete(row: any) {
    this.showConfirm(row.title, row.uuid);
  }

  onEdit(row: any) {
    this.showModalEdit(row.uuid);
  }

  onAdd() {
    this.showModal();
  }
changeFile(){
  if(this.form.value.type == "Pdf" || this.form.value.type == "Image"){
    this.isVisible = true
  }else{
    this.isVisible = false
  }
}
  async submitForm(){
    if (this.form.valid) {
      const data = {
        title: this.form.value.title, 
        auteur: this.form.value.auteur,
        type: this.form.value.type,
        url_file: this.uploadedFile,
        description: this.form.value.description,
        expiration_date: this.form.value.expiration,
      }

      this.isConfirmLoading = true
      if (this.isEdit){
        await this.service.updateData(this.uuid, data).toPromise()
        this.datatable.fetchData()
      }else{
        if(this.isVisible){
          let formData = new FormData();
          formData.append("uploaded_file", this.uploadedFile)
          this.http.post<any>(`${BASE_URL}/upload?namefile=`+this.form.value.title,formData).subscribe(
            async(data) => {
              if(data){
                const body = {
                  title: this.form.value.title, 
                  auteur: this.form.value.auteur,
                  type: this.form.value.type,
                  url_file: data.filename,
                  description: this.form.value.description,
                  expiration_date: this.form.value.expiration,
                }
                await this.service.addData(body).toPromise()
                this.datatable.fetchData()
              }
            }, 
            error => console.error("error as ", error)
            )
        }else{
          await this.service.addData(data).toPromise()
          this.datatable.fetchData()
        }
      }
      
      this.isvisible = false,
      this.isConfirmLoading = false
    } else {
      Object.values(this.form.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
    }
  }

  showModal(): void{
    this.isEdit = false;
    this.isvisible = true;
    this.form.get('name')?.setValue('');
    this.form.get('capacity')?.setValue('');
  }

  async showModalEdit(uuid: string){
    this.isEdit = true
    this.uuid = uuid
    
    let data: Publication = await this.service.getData(uuid).toPromise()
    this.form.get('title')?.setValue(data.title),
    this.form.get('auteur')?.setValue(data.auteur),
    this.form.get('description')?.setValue(data.description),
    this.form.get('expiration')?.setValue(data.expiration_date),
    this.form.get('type')?.setValue(data.type)
    this.isvisible = true
  }


  handleCancel(): void{
    this.isvisible = false
  }

  handleOk(): void{
    setTimeout(() => {
      this.isvisible = false
      this.isConfirmLoading = false
    }, 3000);
  }
  selectFile(event: any){
    if(!event.target.files[0] || event.target.files[0].length == 0){
      this.msg = "select a file"
      this.disabled = true
    }else{
    this.disabled = false
    }
    var mineType = event.target.files[0].type;
    if(mineType.match(/document\/*/) == null){
      this.msg = "select image"
    }
    var reader = new FileReader();
    reader.readAsDataURL(event.target.files[0])

    reader.onload = (_event) =>{
      this.msg = ""
      this.url = reader.result
    } 
    this.uploadedFile = event.target.files[0]
    this.disabled = false
   }

}
