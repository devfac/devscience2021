import { AfterContentInit, Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { QueryParams, otherQueryParams } from '@app/models/query';
import { TableHeader, TableHeaderType } from '@app/models/table';
import { AuthService } from '@app/services/auth/auth.service';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils';
import { CollegeYearService } from '../../home/college-year/college-year.service';
import { JourneyService } from '../../home/journey/journey.service';
import { MentionService } from '../../home/mention/mention.service';
import { SelectionService } from '../selection/selection.service';
import { typeEtudiant,typeSerie, typeSex, typeNation, typeSituation } from '@app/data/data';

const CODE = "upload"
@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.less']
})
export class UploadComponent implements OnInit ,AfterContentInit{
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  @ViewChild('sexTemplate',{static: true}) sex!: TemplateRef<any>;
  @ViewChild('nationTemplate',{static: true}) nation!: TemplateRef<any>;
  @ViewChild('baccTemplate',{static: true}) baccSerie!: TemplateRef<any>;
  @ViewChild('semesterTemplate',{static: true}) semester!: TemplateRef<any>;
  @ViewChild('typeTemplate',{static: true}) type!: TemplateRef<any>;
  @ViewChild('situationTemplate',{static: true}) situation!: TemplateRef<any>;
  headers: TableHeader[] = [];

  user = localStorage.getItem('user')
  allYears: CollegeYear[] = []
  listOfSemester = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  allJourney: Journey[] = []
  allMention: Mention[] = []
  form!: FormGroup;
  formList!: FormGroup
  keyYear = CODE+"collegeYear"
  keyMention = CODE+"mention"
  keyJourney = CODE+"journey"
  isLoading: boolean = false
  typeSex = typeSex
  typeNation=typeNation
  typeSerie=typeSerie
  typeEtudiant=typeEtudiant
  typeSituation=typeSituation

  constructor(
    private fb: FormBuilder, 
    private service: SelectionService,
    private authUser: AuthService,
    private serviceJourney: JourneyService,
    private serviceMention: MentionService,
    private serviceYears: CollegeYearService,) { 
      this.form = this.fb.group({
        mention: [null, Validators.required],
        collegeYear: [null, Validators.required],
        journey: [null, Validators.required],
      });}

  ngAfterContentInit(): void {
    this.headers = [
      {
        title: 'Num Carte',
        selector: 'num_carte',
        width:'120px',
        type: TableHeaderType.LEFT,
        isSortable: false,
    },
    {
        title: 'Nom',
        selector: 'last_name',
        width:'200px',
        isSortable: false,
    },
    {
        title: 'Prénom',
        selector: 'first_name',
        isSortable: false,
    },
    {
        title: 'Date de Naissance',
        selector: 'date_birth',
        isSortable: false,
    },
    {
        title: 'Lieu de Naissance',
        selector: 'place_birth',
        isSortable: false,
    },
    {
        title: 'Adresse',
        selector: 'address',
        isSortable: false,
    },
    {
        title: 'Sexe',
        selector: 'sex',
        template: this.sex,
        isSortable: false,
    },
    {
        title: 'Nation',
        selector: 'nation',
        template: this.nation,
        isSortable: false,
    },
    {
        title: 'Series Bacc ',
        selector: 'baccalaureate_series',
        template: this.baccSerie,
        isSortable: false,
    },
    {
        title: 'Semestre inf',
        selector: 'baccalaureate_series',
        template: this.semester,
        isSortable: false,
    },
    {
        title: 'Semestre sup ',
        selector: 'baccalaureate_series',
        template: this.semester,
        isSortable: false,
    },
    {
        title: 'Etat ',
        selector: 'type',
        template: this.type,
        isSortable: false,
    },
    {
      title: 'Situation ',
      selector: 'situation',
      template: this.situation,
      isSortable: false,
  },
    ]
  }

  async ngOnInit() {

    const user = this.authUser.userValue
    for(let i=0; i<user?.uuid_mention.length;i++){
      let mention = await this.serviceMention.getData(user?.uuid_mention[i]).toPromise()
      this.allMention.push(mention)
          
    }
    
    this.allYears = await this.serviceYears.getDataPromise().toPromise()
    
    if(this.testStorage(this.keyMention, this.allMention[0].uuid) && 
    this.testStorage(this.keyYear, this.allYears[0].title)){
      let uuidMention = localStorage.getItem(this.keyMention)
      if(uuidMention !== null){
        this.allJourney = await this.serviceJourney.getDataByMention(uuidMention).toPromise()}
        this.fetchData = this.fetchData.bind(this)
        this.isLoading = true
    }
  }

  getAllStudents(): void{
    if(this.form.get(this.keyYear.substring(CODE.length))?.value && 
    this.form.get(this.keyMention.substring(CODE.length))?.value && this.isLoading){
      localStorage.setItem(this.keyYear, this.form.get(this.keyYear.substring(CODE.length))?.value)
      localStorage.setItem(this.keyMention, this.form.get(this.keyMention.substring(CODE.length))?.value)
      this.datatable.fetchData()
    }
  }

  fetchData(params?: QueryParams){
    let otherParams: otherQueryParams = {
      college_year: localStorage.getItem(this.keyYear),
      uuid_mention: localStorage.getItem(this.keyMention),
    }
    return this.service.getDataObservable(parseQueryParams(params,otherParams))
  }


  testStorage(key: string, value: string): boolean{
    if(localStorage.getItem(key)){
      this.form.get(key.substring(CODE.length))?.setValue(localStorage.getItem(key))
    }else{
      localStorage.setItem(key, value)
      this.form.get(key.substring(CODE.length))?.setValue(localStorage.getItem(key))
    }
    console.log(key.substring(CODE.length), value)
    return true
  }
}
