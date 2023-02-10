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
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { head } from 'lodash';

const BASE_URL = environment.authApiURL;


@Component({
  selector: 'app-publication',
  templateUrl: './publication.component.html',
  styleUrls: ['./publication.component.less']
})
export class PublicationComponent implements OnInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];
   
  private headersParams =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+window.sessionStorage.getItem("token")
  })
  user = window.sessionStorage.getItem('user')
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
  files: any[] = [];
  validFiles: boolean = false

  msg!: string ;
  url: string | ArrayBuffer | null = "";
  uploadedFile: any[] = [];

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
    this.validFile()
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
          console.log(this.uploadedFile);
          for(let i=0; i<this.uploadedFile.length; i++){
            formData.append("uploaded_files", this.uploadedFile[i])
          }
          
          this.http.post<any>(`${BASE_URL}/upload/?name_file=`+this.form.value.title,formData, {headers: this.headersParams}).subscribe(
            async(data) => {
              if(data){
                console.log(data);
                const body = {
                  title: this.form.value.title, 
                  auteur: this.form.value.auteur,
                  type: this.form.value.type,
                  url_file: data.filenames,
                  description: this.form.value.description,
                  expiration_date: this.form.value.expiration,
                }
                await this.service.addData(body).toPromise()
                this.datatable.fetchData()
                this.files = []
                this.uploadedFile = []
              }
            }, 
            error => console.error("error as ", error)
            )
        }else{
          await this.service.addData(data, ).toPromise()
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
    this.form.get('title')?.setValue(''),
    this.form.get('auteur')?.setValue(''),
    this.form.get('description')?.setValue(''),
    this.form.get('expiration')?.setValue(''),
    this.form.get('type')?.setValue('')
    this.changeFile()
    this.isvisible = true;
  }

  async showModalEdit(uuid: string){
    this.isEdit = true
    this.uuid = uuid
    this.uploadedFile = []
    this.files = []
    let data: Publication = await this.service.getData(uuid).toPromise()
    this.form.get('title')?.setValue(data.title),
    this.form.get('auteur')?.setValue(data.auteur),
    this.form.get('description')?.setValue(data.description),
    this.form.get('expiration')?.setValue(data.expiration_date),
    this.form.get('type')?.setValue(data.type)
    for (var file of data.url_file){
      this.files.push(`${BASE_URL}/upload/?name_file=`+file)
      this.uploadedFile.push(`${BASE_URL}/upload/?name_file=`+file)
    }
    this.changeFile()
    this.isvisible = true
  }

  setName(name: string): string{
    if(name?.length > 40){
      return name.substring(0,40)+"..."+name.substring(name.length -5,name.length)
    }
    return name
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
    /**
   * on file drop handler
   */
  onFileDropped(event: any) {
    this.prepareFilesList(event);
  }

  /**
   * handle file from browsing
   */
  fileBrowseHandler(event: any) {
    this.prepareUploadFile(event?.target.files[0]);
    this.prepareFilesList(event?.target.files);
    
  }
  validFile(){
    if(this.form.value.type !== "Text" && this.form.value.type !== "Other"){
      if(this.uploadedFile.length > 0)
        this.validFiles= true
      else
      this.validFiles= false
    }else{
      this.validFiles= true
    }
    console.log(this.validFiles);
    
  }
  /**
   * Delete file from files list
   * @param index (File index)
   */
  deleteFile(index: number) {
    this.files.splice(index, 1);
    this.uploadedFile.splice(index, 1);
    this.validFile()
  }

  /**
   * Simulate the upload process
   */
  uploadFilesSimulator(index: number) {
  this.validFile()
    setTimeout(() => {
      if (index === this.files.length) {
        return;
      } else {
        const progressInterval = setInterval(() => {
          if (this.files[index].progress === 100) {
            clearInterval(progressInterval);
            this.uploadFilesSimulator(index + 1);
          } else {
            this.files[index].progress += 5;
          }
        }, 200);
      }
    }, 1000);
  }

  /**
   * Convert Files list to normal array list
   * @param files (Files List)
   */
  prepareFilesList(files: Array<any>) {
    for (const item of files) {
      item.progress = 0;
      this.files.push(item);
    }
    this.uploadFilesSimulator(0);

  }

  prepareUploadFile(files: any){
    this.uploadedFile.push(files)
  }

  /**
   * format bytes
   * @param bytes (File size in bytes)
   * @param decimals (Decimals point)
   */
  formatBytes(bytes: number, decimals: number) {
    if (bytes === 0) {
      return '0 Bytes';
    }
    const k = 1024;
    const dm = decimals <= 0 ? 0 : decimals || 2;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }

}
