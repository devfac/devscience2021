import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { otherQueryParams, QueryParams } from '@app/models/query';
import { AncienStudent, ColumnItem, StudentColumn } from '@app/models/student';
import { TableHeader } from '@app/models/table';
import { AuthService } from '@app/services/auth/auth.service';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { CollegeYearService } from '../../home/college-year/college-year.service';
import { JourneyService } from '../../home/journey/journey.service';
import { MentionService } from '../../home/mention/mention.service';
import { InscriptionService } from './inscription.service';

const CODE = "inscription"

@Component({
  selector: 'app-inscription',
  templateUrl: './inscription.component.html',
  styleUrls: ['./inscription.component.less']
})
export class InscriptionComponent implements OnInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];


  user = localStorage.getItem('user')
  allYears: CollegeYear[] = []
  allStudents: AncienStudent[] = []
  allJourney: Journey[] = []
  allMention: Mention[] = []
  listOfSemester = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  semesterTitles: any[] = []
  confirmModal?: NzModalRef
  form!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  data = ""
  uuid= "";
  listOfData: any[] = []
  keyMention = CODE+"mention"
  keyYear = CODE+"collegeYear"

  actions = {
    add: true,
    edit: true,
    delete: true,
    detail: false,
  };
  
  constructor(
    private modal: NzModalService, 
    private fb: FormBuilder, 
    public router: Router, 
    private authUser: AuthService, 
    private serviceJourney: JourneyService,
    private serviceMention: MentionService,
    private serviceYears: CollegeYearService,
    private service: InscriptionService,
    ) { 


    this.form = this.fb.group({
      email: [null, [Validators.required]],
      firstName: [null, [Validators.required]],
      lastName: [null, [Validators.required]],
      isAdmin: [false],
      mention: [null],
      collegeYear: [null],
      uuidRole: [null, [Validators.required]],
      uuidMention: [[], [Validators.required]],
      filter: [null],
    });
  }


  ngAfterContentInit(): void {
    this.headers = [
    {
      title: 'Num Select',
      selector: 'num_select',
      isSortable: true,
    },{
      title: 'Nom',
      selector: 'last_name',
      isSortable: true,
    },{
      title: 'Prenom',
      selector: 'first_name',
      isSortable: true,
    },{
      title: 'Niveau',
      selector: 'level',
      isSortable: true,
    },{
      title: 'Parcours',
      selector: 'journey.abbreviation',
      isSortable: true,
    },
  ];
  }

 async ngOnInit() {
  this.fetchData = this.fetchData.bind(this)

    const user = this.authUser.userValue
    for(let i=0; i<user?.uuid_mention.length;i++){
      let mention = await this.serviceMention.getData(user?.uuid_mention[i]).toPromise()
      this.allMention.push(mention)
          
    }


    for(let i=0; i<this.listOfSemester.length; i++){
      this.semesterTitles.push(
        {
          text: this.listOfSemester[i], value: this.listOfSemester[i]
        }
      )
    }
    
    this.allYears = await this.serviceYears.getDataPromise().toPromise()
    this.testStorage('collegeYear', this.allYears[0].title)
  
    this.allJourney = await this.serviceJourney.getDataByMention(localStorage.getItem(this.keyMention)).toPromise()
  }

  
  testStorage(key: string, value: string){
    if(localStorage.getItem(key)){
      this.form.get(key)?.setValue(localStorage.getItem(key))
    }else{
      localStorage.setItem(key, value)
      this.form.get(key)?.setValue(localStorage.getItem(key))
    }
  }

  fetchData(params?: QueryParams){
    let otherParams: otherQueryParams = {
      college_year: localStorage.getItem(this.keyYear),
      uuid_mention: localStorage.getItem(this.keyMention),
    }
    return this.service.getDataObservable(parseQueryParams(params,otherParams))
  }
  showConfirm(name: string, numSelect: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: async () => {
        await this.service.deletData(numSelect)
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
    this.addStudent();
  }
  
  showModalEdit(numSelect: string): void{
    this.isEdit = true
    localStorage.setItem('numSelect', numSelect)
    localStorage.setItem("uuid_mention", this.form.get("mention")?.value)
    localStorage.setItem("college_years", this.form.get("collegeYear")?.value)
    this.router.navigate(['/user/inscription_add'])
  }


  handleCancel(): void{
    this.isvisible = false
  }

  getAllStudents(): void{
    if(this.form.get(this.keyYear)?.value && this.form.get(this.keyMention)?.value){this.datatable.fetchData()
    }
  }

  addStudent():void{
    localStorage.setItem("mention", this.form.get("mention")?.value)
    localStorage.setItem("collegeYear", this.form.get("collegeYear")?.value)
    this.router.navigate(['/user/inscription_add'])
    localStorage.setItem('numSelect', '')
  }

  handleOk(): void{
    setTimeout(() => {
      this.isvisible = false
      this.isConfirmLoading = false
    }, 3000);
  }

  changeFilter(){
    if(this.form.value.filter){
      this.listOfData = this.allStudents.filter((item: any) => item.journey.uuid === this.form.value.filter)
    }else{
      this.listOfData = this.allStudents
    }
  }


}
