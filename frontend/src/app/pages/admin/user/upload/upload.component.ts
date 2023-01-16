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
import { UploadService } from './upload.service';
import { ResponseModel } from '@app/models/response';
import { environment } from '@environments/environment';
import { HttpParams } from '@angular/common/http';
import { UtilsService } from '../../utils.service';

const BASE_URL = environment.authApiURL;


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
  formTemplate!: FormGroup
  keyYear = CODE+"collegeYear"
  keyMention = CODE+"mention"
  keyJourney = CODE+"journey"
  isLoading: boolean = false
  typeSex = typeSex
  typeNation=typeNation
  typeSerie=typeSerie
  typeEtudiant=typeEtudiant
  typeSituation=typeSituation
  isConfirmLoading=false
  isvisible=false
  disabled = true
  initialise= false
  initialiseTemplate= false
  url_excel="assets/images/face.png";
  msg!: string ;
  url: string | ArrayBuffer | null = "";
  uploadedFile: any;

  checked = false;
  loading = false;
  indeterminate = false;
  listOfData: readonly any[] = [];
  listOfCurrentPageData: readonly any[] = [];
  setOfCheckedId = new Set<number>();

  constructor(
    private fb: FormBuilder, 
    private service: UploadService,
    private authUser: AuthService,
    private serviceJourney: JourneyService,
    private serviceMention: MentionService,
    private serviceYears: CollegeYearService,
    private utlisService: UtilsService,) { 
      this.form = this.fb.group({
        mention: [null, Validators.required],
        collegeYear: [null, Validators.required],
        journey: [null, Validators.required],
      });
      this.formTemplate = this.fb.group({
        baccalaureate_series: [null],
        inf_semester: [null],
        sup_semester: [null],
        sex: [null],
        nation: [null],
        type: [null],
        situation: [null],
      });
    }

  ngAfterContentInit(): void {
    this.headers = [
      {
        title: 'Num Carte',
        selector: 'num_carte',
        width:'150px',
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
        width:'150px',
        selector: 'first_name',
        isSortable: false,
    },
    {
        title: 'Date de Naissance',
        width:'150px',
        selector: 'date_birth',
        isSortable: false,
    },
    {
        title: 'Lieu de Naissance',
        width:'150px',
        selector: 'place_birth',
        isSortable: false,
    },
    {
        title: 'Adresse',
        width:'150px',
        selector: 'address',
        isSortable: false,
    },
    {
        title: 'Sexe',
        width:'150px',
        selector: 'sex',
        template: this.sex,
        isSortable: false,
    },
    {
        title: 'Nation',
        width:'150px',
        selector: 'nation',
        template: this.nation,
        isSortable: false,
    },
    {
        title: 'Series Bacc ',
        width:'150px',
        selector: 'baccalaureate_series',
        template: this.baccSerie,
        isSortable: false,
    },
    {
        title: 'Semestre inf',
        width:'150px',
        selector: 'inf_semester',
        template: this.semester,
        isSortable: false,
    },
    {
        title: 'Semestre sup ',
        width:'150px',
        selector: 'sup_semester',
        template: this.semester,
        isSortable: false,
    },
    {
        title: 'Etat ',
        width:'150px',
        selector: 'type',
        template: this.type,
        isSortable: false,
    },
    {
      title: 'Situation ',
      width:'150px',
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
    
    let allYears: ResponseModel = await this.serviceYears.getDataPromise().toPromise()
    this.allYears = allYears.data

    
    if(this.testStorage(this.keyMention, this.allMention[0].uuid) && 
    this.testStorage(this.keyYear, this.allYears[0].title)){
      let uuidMention = localStorage.getItem(this.keyMention)
      if(uuidMention !== null){
        this.allJourney = await this.serviceJourney.getDataByMention(uuidMention).toPromise()}
        this.isLoading = true
    }

    this.initialise = true
  }

  async getAllStudents(){
    if(this.form.get(this.keyMention.substring(CODE.length))?.value && this.isLoading){
      this.allJourney = await this.serviceJourney.getDataByMention(this.form.get(this.keyMention.substring(CODE.length))?.value ).toPromise()
    }
  }
  
  changeTemplate(row: any, title:string){
    if (this.initialiseTemplate){
      const value = this.formTemplate.get(title)?.value
      row[title] = value
    }
    
  }
  startDownloadFace(){
    let url: string = `${BASE_URL}/save_data/get_models/`;

    let params = new HttpParams()
      .append('model_name', "student")
    let name: string = 'Model_students'
    this.utlisService.download(url, params, name, ".xlsx");                   
    this.isvisible = false;
  }
  testStorage(key: string, value: string): boolean{
    if(localStorage.getItem(key)){
      this.form.get(key.substring(CODE.length))?.setValue(localStorage.getItem(key))
    }else{
      localStorage.setItem(key, value)
      this.form.get(key.substring(CODE.length))?.setValue(localStorage.getItem(key))
    }
    return true
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

   handleCancel(){
    this.isvisible = false
   }

   showModal(){
    this.isvisible = true
   }

   async submitForm(){
    const formData = new FormData();
    if (this.url !== "" && this.initialise){
      this.isConfirmLoading = true
      formData.append("uploaded_file", this.uploadedFile)
      let listOfData: ResponseModel  = await this.service.uploadFile(formData, "student", this.form.value.mention, this.form.value.journey, this.form.value.collegeYear).toPromise()
      this.listOfData = listOfData.data
      this.isConfirmLoading = false
      this.isvisible = false
      this.initialiseTemplate = true
   }
  }


  getValue(data: any, selector: string) {
    const selectors = selector.split('.');
    return selectors.reduce((a, prop) => a[prop], data);
  }

  updateCheckedSet(num_carte: number, checked: boolean): void {
    if (checked) {
      this.setOfCheckedId.add(num_carte);
    } else {
      this.setOfCheckedId.delete(num_carte);
    }
  }

  onCurrentPageDataChange(listOfCurrentPageData: readonly any[]): void {
    this.listOfCurrentPageData = listOfCurrentPageData;
    this.refreshCheckedStatus();
  }

  refreshCheckedStatus(): void {
    const listOfEnabledData = this.listOfCurrentPageData;
    this.checked = listOfEnabledData.every(({ num_carte }) => this.setOfCheckedId.has(num_carte));
    this.indeterminate = listOfEnabledData.some(({ num_carte }) => this.setOfCheckedId.has(num_carte)) && !this.checked;
  }

  onItemChecked(num_carte: number, checked: boolean): void {
    this.updateCheckedSet(num_carte, checked);
    this.refreshCheckedStatus();
  }

  onAllChecked(checked: boolean): void {
    this.listOfCurrentPageData
      .forEach(({ num_carte }) => this.updateCheckedSet(num_carte, checked));
    this.refreshCheckedStatus();
  }

 async  sendRequest() {
    this.loading = true;
    const requestData = this.listOfData.filter(data => this.setOfCheckedId.has(data.num_carte));
    let listOfData: ResponseModel  = await this.service.saveData(requestData, this.form.value.mention, this.form.value.journey, this.form.value.collegeYear).toPromise()
    this.listOfData = listOfData.data
    console.log(requestData);
    setTimeout(() => {
      this.setOfCheckedId.clear();
      this.refreshCheckedStatus();
      this.loading = false;
    }, 1000);
  }
  trackByIdSelector(_: number, item: any): string {
    return item["num_carte"];
  }
}
