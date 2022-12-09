import { AfterContentInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { otherQueryParams, QueryParams } from '@app/models/query';
import { ResponseModel } from '@app/models/response';
import { TableHeader } from '@app/models/table';
import { Ue } from '@app/models/ue';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { CollegeYearService } from '../college-year/college-year.service';
import { JourneyService } from '../journey/journey.service';
import { MentionService } from '../mention/mention.service';
import { UeService } from './ue.service';


@Component({
  selector: 'app-ue',
  templateUrl: './ue.component.html',
  styleUrls: ['./ue.component.less']
})
export class UeComponent implements OnInit, AfterContentInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];

  user = localStorage.getItem('user')
  allJourney: Journey[] = []
  allJourneyList: Journey[] = []
  allMention: Mention[] = []
  allUe: Ue[] = []
  listOfSemester = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  semesterTitles: any[] = []
  confirmModal?: NzModalRef;
  form!: FormGroup;
  formList!: FormGroup;
  form_years!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  uuid= "";
  actualYear: string | null = ""
  titles: any[] = []
  actions = {
    add: true,
    edit: true,
    delete: true,
    detail: false,
  };
  
  isInit: boolean = false
  constructor(
    private modal: NzModalService, 
    private fb: FormBuilder,
    private serviceJourney: JourneyService,
    private serviceMention: MentionService,
    private serviceYears: CollegeYearService,
    private service: UeService
    ) { 
      this.form = this.fb.group({
        title: [null, [Validators.required]],
        semester: [null, [Validators.required]],
        journey: [null, [Validators.required]],
        credit: [null, [Validators.required]],
        mention: [null, [Validators.required]],
        collegeYear: [null],
      });
      this.formList = this.fb.group({
        mention: [null],
        semester: [null],
        journey: [null],
      })
    }
      

  async ngAfterContentInit() {
    this.headers = [
    {
      title: 'Title',
      selector: 'title',
      isSortable: true,
    },{
      title: 'Parcours',
      selector: 'abbreviation_journey',
      isSortable: false,
    },{
      title: 'Semestre',
      selector: 'semester',
      isSortable: true,
    },{
      title: 'Credit',
      selector: 'credit',
      isSortable: true,
    },
  ];

  }

  async ngOnInit(){
    this.fetchData = this.fetchData.bind(this)

    let allMention: ResponseModel = await this.serviceMention.getDataPromise().toPromise()
    this.allMention = allMention.data
    this.testStorage('mention', this.allMention[0].uuid)

    this.allJourney = await this.serviceJourney.getDataByMention(this.form.get('mention')?.value).toPromise()
    let journey: ResponseModel = await this.serviceJourney.getDataPromise().toPromise()
    this.allJourneyList = journey.data
    this.testStorage('journey', this.allJourney[0].uuid)
    
    for(let i=0; i<this.listOfSemester.length; i++){
      this.semesterTitles.push(
        {
          text: this.listOfSemester[i], value: this.listOfSemester[i]
        }
      )
    }
  }
  fetchData(params?: QueryParams){
    let otherParams: otherQueryParams = {
      uuid_journey: localStorage.getItem('journey'),
      semester: localStorage.getItem("semester"),
    }
    return this.service.getDataObservable(parseQueryParams(params, otherParams))
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

  async submitForm(){
    if (this.form.valid) {
      const data = {credit: this.form.value.credit}

      this.isConfirmLoading = true
      console.error(data)
      if (this.isEdit){
        this.form.get('title')?.disabled
        await this.service.updateData(this.uuid, data).toPromise()
        this.datatable.fetchData()
      }else{
        const data = {
          title: this.form.value.title,
          credit: this.form.value.credit,
          value: "",
          key_unique: "",
          uuid_journey: this.form.value.journey,
          semester: this.form.value.semester
        }
        await this.service.addData(data).toPromise()
        this.datatable.fetchData()
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
    this.form.get('title')?.setValue('');
    this.form.get('credit')?.setValue('');
    this.form.get('journey')?.setValue('');
    this.form.get('semester')?.setValue('');
  }

  async showModalEdit(uuid: string){
    this.isEdit = true
    this.uuid = uuid
    
    let data: any = await this.service.getData(uuid).toPromise()
    this.form.get('title')?.setValue(data.title),
    this.form.get('credit')?.setValue(data.credit),
    this.form.get('journey')?.setValue(data.journey.uuid),
    this.form.get('mention')?.setValue(data.journey.uuid_mention),
    this.form.get('semester')?.setValue(data.semester)
    if(this.form.get('mention')?.value){
      this.allJourney = await this.serviceJourney.getDataByMention(this.form.get('mention')?.value).toPromise()
    }

    this.isvisible = true
  }

  async getAllJourney(){
    if(this.form.get('mention')?.value){
      this.allJourney = await this.serviceJourney.getDataByMention(this.form.get('mention')?.value).toPromise()
    }
  }

  changeJourney(){
    if(this.formList.value.journey ){
        const journey = this.allJourneyList.find((item: Journey) => item.uuid === this.formList.value.journey)
        if (journey){
        this.listOfSemester = journey.semester
        localStorage.setItem("journey", this.formList.value.journey)
        this.datatable.fetchData()
      }
      }else{
        localStorage.setItem("journey", this.formList.value.journey)
        this.datatable.fetchData()
      }
    }

  changeSemester(){
    localStorage.setItem("semester", this.formList.value.semester)
    this.datatable.fetchData()
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
}
