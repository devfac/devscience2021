import { AfterContentInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CollegeYear } from '@app/models/collegeYear';
import { Ec } from '@app/models/ec';
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
import { UeService } from '../ue/ue.service';
import { EcService } from './ec.service';


@Component({
  selector: 'app-ec',
  templateUrl: './ec.component.html',
  styleUrls: ['./ec.component.less']
})
export class EcComponent implements OnInit, AfterContentInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];

  user = localStorage.getItem('user')
  collegeYear = localStorage.getItem('collegeYear')
  allYears: CollegeYear[] = []
  allJourney: Journey[] = []
  allJourneyList: Journey[] = []
  allMention: Mention[] = []
  allEc: Ec[] = []
  allUe: Ue[] = []
  listOfSemester = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  semesterTitles: any[] = []
  confirmModal?: NzModalRef;
  form!: FormGroup;
  formList!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  uuid= "";
  data = ""
  initialise: boolean = false
  actualYear: string | null = ""
  titles: any[] = []
  actions = {
    add: true,
    edit: true,
    delete: true,
    detail: false,
  };


  constructor(
    private modal: NzModalService, 
    private fb: FormBuilder,
    private service: EcService,
    private serviceJourney: JourneyService,
    private serviceMention: MentionService,
    private serviceYears: CollegeYearService,
    private serviceUe: UeService
    ) { 
    this.form = this.fb.group({
    title: [null, [Validators.required]],
    semester: [null, [Validators.required]],
    valueUe: [null, [Validators.required]],
    journey: [null, [Validators.required]],
    weight: [null, [Validators.required]],
    uuidMention: [null, [Validators.required]],
    isOptional: [null],
    user: [null, ],
    collegeYear: [null],
  });
  this.formList = this.fb.group({
    semester: [null],
    journey: [null],
   
  });
}
  ngAfterContentInit(): void {
    this.headers = [
    {
      title: 'Title',
      selector: 'title',
      width: "190px",
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
      title: 'Ue',
      selector: 'value_ue',
      isSortable: true,
    },{
      title: 'Poids',
      selector: 'weight',
      isSortable: true,
    },
  ];
  }

  async ngOnInit(){
    this.fetchData = this.fetchData.bind(this)

    let allMention: ResponseModel = await this.serviceMention.getDataPromise().toPromise()
    this.allMention = allMention.data
    this.testStorage('mention', this.allMention[0].uuid)

    this.allJourney = await this.serviceJourney.getDataByMention(localStorage.getItem('mention')!).toPromise()
    let journey: ResponseModel = await this.serviceJourney.getDataPromise().toPromise()
    this.allJourneyList = journey.data
    
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
      nzOnOk: async() => {
        await this.service.deletData(uuid)
        this.datatable.fetchData()
        }
      })
    }

    onDelete(row: any) {
      this.showConfirm(row.title+" "+row.semester+" "+row.journey.abbreviation, row.uuid);
    }

    onEdit(row: any) {
      this.showModalEdit(row.uuid);
    }

    onAdd() {
      this.showModal();
    }
  
  async submitForm(){
    if (this.form.valid) {
      const data = {
        title: this.form.value.title,
        uuid_journey: this.form.value.journey,
        weight: this.form.value.weight,
        semester: this.form.value.semester,
        value_ue: this.form.value.valueUe,
        teacher: this.form.value.user,
        value: "",
        key_unique: "",
        is_optional: this.form.value.isOptional
      }
      this.isConfirmLoading = true
      console.error(data)
      if (this.isEdit){
        await this.service.updateData(this.uuid, data).toPromise()
        this.datatable.fetchData()
      }else{
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
    this.form.reset()
    this.form.get('collegeYear')?.setValue(localStorage.getItem('year'))
    this.form.get('isOptional')?.setValue(false)
  }

  async showModalEdit(uuid: string){
    this.isEdit = true
    this.uuid = uuid
    let data: any = await this.service.getData(uuid).toPromise()
    this.form.get('uuidMention')?.setValue(data.journey.uuid_mention)
    this.form.get('journey')?.setValue(data.journey.uuid)
    this.form.get('title')?.setValue(data.title),
    this.form.get('weight')?.setValue(data.weight),
    this.form.get('semester')?.setValue(data.semester)
    this.form.get('valueUe')?.setValue(data.value_ue)
    this.form.get('user')?.setValue(data.users)
    this.form.get('isOptional')?.setValue(data.is_optional)

    if(this.form.get('uuidMention')?.value){
      this.allJourney = await this.serviceJourney.getDataByMention(this.form.get('uuidMention')?.value).toPromise()
    }

    if (this.form.get('journey')?.value && this.form.get('semester')?.value){
      this.allUe = await this.serviceUe.getDataPromise(this.form.get('semester')?.value, this.form.get('journey')?.value).toPromise()
    }

    this.isvisible = true
  }
 async getAllUe(){
    if (this.form.get('journey')?.value && this.form.get('semester')?.value){
      this.allUe = await this.serviceUe.getDataPromise(this.form.get('semester')?.value, this.form.get('journey')?.value).toPromise()}
  }
  async getAllJourney(){
    if(this.form.get('uuidMention')?.value){
      this.allJourney = await this.serviceJourney.getDataByMention(this.form.get('uuidMention')?.value).toPromise()
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
