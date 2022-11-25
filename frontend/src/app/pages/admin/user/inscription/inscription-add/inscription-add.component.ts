import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { typeSex, typeNation, typeSituation, typeSerie } from '@app/data/data';
import { CollegeYear } from '@app/models/collegeYear';
import { Droit } from '@app/models/droit';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { Receipt } from '@app/models/receipt';
import { CollegeYearService } from '@app/pages/admin/home/college-year/college-year.service';
import { JourneyService } from '@app/pages/admin/home/journey/journey.service';
import { MentionService } from '@app/pages/admin/home/mention/mention.service';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { UserService } from '../../user.service';
import { InscriptionService } from '../inscription.service';

const CODE = "inscription"
const BASE_URL = environment.authApiURL;


@Component({
  selector: 'app-inscription-add',
  templateUrl: './inscription-add.component.html',
  styleUrls: ['./inscription-add.component.less']
})
export class InscriptionAddComponent implements OnInit {

  allYear: CollegeYear[] = []
  confirmModal?: NzModalRef;
  form!: FormGroup;
  formDialog!: FormGroup
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  uuid= "";
  url:any ="assets/images/profil.png";
  msg= "";
  isDisabled: boolean = false
  allMention: Mention[] = []
  allJourney: Journey[] = []
  allPrice: Droit[] = []
  allReceipt: Receipt[] = []
  typeSex = typeSex
  typeSituation = typeSituation
  typeNation = typeNation
  typeSerie = typeSerie
  isReady: boolean = false

  keyMention = CODE+"mention"
  keyYear = CODE+"collegeYear"
  keyNum = CODE+"numSelect"

  defaultValue = {
      journey:"6b877d4c-dd5b-4efa-9a2e-3871027067e8",
      baccYear: "2020",
      situation: "Célibataire",
      telephone: "",
      baccNum: this.makeRandom(8),
      baccCenter: this.makeRandom(12),
      baccSerie: "Serie C",
      work: this.makeRandom(6),
      fatherName: this.makeRandom(12)+" "+this.makeRandom(8),
      fatherWork: this.makeRandom(8),
      motherName: this.makeRandom(12)+" "+this.makeRandom(8),
      motherWork: this.makeRandom(8),
      parentAddress: this.makeRandom(12)+" "+this.makeRandom(3),

  }
  setDefaultValueForm: () => void;
  blob = new Blob(["assets/images/profil.png"])
  uploadedImage: File = new File([this.blob], 'profile.png');

  constructor(
    private http: HttpClient, 
    private modal: NzModalService, 
    private fb: FormBuilder, 
    private service: UserService, 
    private inscriptionService: InscriptionService,
    private serviceJourney: JourneyService,
    private serviceMention: MentionService,
    public router: Router ) {

    this.form = this.fb.group({
      mention: [null, [Validators.required]],
      journey: [null, [Validators.required]],
      numSelect: [null, [Validators.required]],
      firstName: [null],
      lastName: [null, [Validators.required]],
      address: [null, [Validators.required]],
      nation: [null, [Validators.required]],
      phone: [null],
      dateBirth: [null, [Validators.required]],
      placeBirth: [null, [Validators.required]],
      sex: [null, [Validators.required]],
      numCin: [null],
      dateCin: [null],
      placeCin: [null],
      receipt: [null, [Validators.required]],
      baccYear: [null, [Validators.required]],

      situation: [null, [Validators.required]],
      telephone: [null],
      baccNum: [null, [Validators.required]],
      baccCenter: [null, [Validators.required]],
      baccSerie: [null, [Validators.required]],
      work: [null, [Validators.required]],
      fatherName: [null],
      fatherWork: [null],
      motherName: [null],
      motherWork: [null],
      parentAddress: [null],

    });

    this.formDialog = this.fb.group({
      priceRigth: [null, [Validators.required]],
      numReceipt: [null, [Validators.required]],
      dateReceipt: [null, [Validators.required]]
    })


    this.setDefaultValueForm = () => this.service.setDefaultValueForm(this.form, this.defaultValue);

   }

   selectFile(event: any){
    if(!event.target.files[0] || event.target.files[0].length == 0){
      this.msg = "select image"
    }
    var mineType = event.target.files[0].type;
    if(mineType.match(/image\/*/) == null){
      this.msg = "select image"
      this.url ="assets/images/profil.png";
    }
    var reader = new FileReader();
    reader.readAsDataURL(event.target.files[0])

    reader.onload = (_event) =>{
      this.msg = ""
      this.url = reader.result
    } 
    this.uploadedImage = event.target.files[0]
   }

  async ngOnInit(){
    const numSelect = localStorage.getItem(this.keyNum)
    if(numSelect && numSelect.length>0){
      this.isEdit = true
      let  data = await this.inscriptionService.getStudentByNumSelect(numSelect).toPromise()
          this.form.get('numSelect')?.setValue(data.num_select)
          this.form.get('mention')?.setValue(data.uuid_mention)
          this.form.get('journey')?.setValue(data.journey.uuid)
          this.form.get('firstName')?.setValue(data.first_name)
          this.form.get('lastName')?.setValue(data.last_name)
          this.form.get('address')?.setValue(data.address)
          this.form.get('dateBirth')?.setValue(data.date_birth)
          this.form.get('placeBirth')?.setValue(data.place_birth)
          this.form.get('sex')?.setValue(data.sex)
          this.form.get('dateCin')?.setValue(data.date_cin)
          this.form.get('placeCin')?.setValue(data.place_cin)
          this.form.get('numCin')?.setValue(data.num_cin)
          this.form.get('sex')?.setValue(data.sex)
          this.form.get('dateCin')?.setValue(data.date_cin)
          this.form.get('placeCin')?.setValue(data.place_cin)
          this.form.get('baccYear')?.setValue(data.baccalaureate_years)
          this.form.get('nation')?.setValue(data.nation)
          this.form.get('receipt')?.setValue(data.receipt.num)
          this.formDialog.get('numReceipt')?.setValue(data.receipt.num)
          this.formDialog.get('dateReceipt')?.setValue(data.receipt.date)
          this.formDialog.get('priceRigth')?.setValue(data.receipt.price)

          this.form.get('situation')?.setValue(data.situation)
          this.form.get('telephone')?.setValue(data.telephone)
          this.form.get('baccNum')?.setValue(data.baccalaureate_center)
          this.form.get('baccCenter')?.setValue(data.baccalaureate_center)
          this.form.get('baccSerie')?.setValue(data.baccalaureate_series)
          this.form.get('work')?.setValue(data.work)
          this.form.get('fatherName')?.setValue(data.father_name)
          this.form.get('fatherWork')?.setValue(data.father_work)
          this.form.get('motherName')?.setValue(data.mother_name)
          this.form.get('motherWork')?.setValue(data.mother_work)
          this.form.get('parentAddress')?.setValue(data.parent_address)
          if (data.photo){
            this.url = `${BASE_URL}/student/photo?name_file=`+data.photo
          }
    }else{
      this.isEdit=false
    }
    let uuidMention = localStorage.getItem(this.keyMention.substring(CODE.length))
    if (uuidMention !== null){
      this.allJourney = await this.serviceJourney.getDataByMention(uuidMention).toPromise()
      this.allMention.push(await this.serviceMention.getData(uuidMention).toPromise())
      this.isReady = true
    }

    this.http.get<Droit[]>(`${BASE_URL}/droit/by_mention?uuid_mention=`+
      localStorage.getItem("mention")+'&year='+localStorage.getItem("collegeYear")).subscribe(
      data =>{ 
        this.allPrice=data
      },
      error => console.error("error as ", error)
    );
  }


  validReceipt(): void{
    if(this.formDialog.valid){
      let data = {
        num: this.formDialog.get('numReceipt')?.value,
        date: this.formDialog.get('dateReceipt')?.value,
        price: this.formDialog.get('priceRigth')?.value,
      }
      this.form.get('receipt')?.setValue(data.num)
      this.isvisible = false
    } else {
      Object.values(this.formDialog.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
    }
  }
  
  async submitForm(){
    if (this.form.valid) {
      const title = this.form.value.title
      const mean = this.form.value.mean
      this.isConfirmLoading = true
      let photo = null
      const formData = new FormData();
      if (this.url !== "assets/images/profil.png"){
        formData.append("uploaded_file", this.uploadedImage)
       let data = await this.service.uploadPhoto(this.form, formData).toPromise()
       if (data.filename){
        photo = data.filename
       }
      }
      const body = 
        {
          last_name: this.form.value.lastName,
          first_name: this.form.value.firstName,
          date_birth: this.form.value.dateBirth,
          place_birth: this.form.value.placeBirth,
          address: this.form.value.address,
          sex: this.form.value.sex,
          nation: this.form.value.nation,
          num_cin: this.form.value.numCin,
          date_cin: this.form.value.dateCin,
          place_cin: this.form.value.placeCin,
          uuid_mention: this.form.value.mention,
          actual_years: localStorage.getItem('college_years'),
          num_select: this.form.value.numSelect,
          receipt: {
            num: this.formDialog.get('numReceipt')?.value,
            date: this.formDialog.get('dateReceipt')?.value,
            price: this.formDialog.get('priceRigth')?.value,
            year: localStorage.getItem('college_years')
          },
          receipt_list: [],
          mean: this.form.value.mean,
          baccalaureate_years: this.form.value.baccYear,

          type: "Passant",
          photo: photo,
          uuid_journey: this.form.value.journey,

          situation: this.form.value.situation,
          telephone: this.form.value.telephone,
          baccalaureate_num: this.form.value.baccNum,
          baccalaureate_center: this.form.value.baccCenter,
          baccalaureate_series: this.form.value.baccSerie,
          work: this.form.value.work,
          father_name: this.form.value.fatherName,
          father_work: this.form.value.fatherWork,
          mother_name: this.form.value.motherName,
          mother_work: this.form.value.motherWork,
          parent_address: this.form.value.parentAddress,

        }
        await this.inscriptionService.updateData(this.form.value.numSelect, body).toPromise()
        this.router.navigate(['/user/inscription'])
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
    this.isvisible = true;
    console.error(this.form.get('receipt')?.value)
    if(!this.form.get('receipt')?.value){

      this.formDialog.reset()
    }
  }

  async getStudentByNumSelect(){
    const numSelect = this.form.get('numSelect')?.value
    if(numSelect && numSelect.length>0){
      let  data = await this.inscriptionService.getStudentByNumSelect(numSelect).toPromise()
        this.form.get('mention')?.setValue(data.uuid_mention)
        this.form.get('firstName')?.setValue(data.first_name)
        this.form.get('lastName')?.setValue(data.last_name)
        this.form.get('address')?.setValue(data.address)
        this.form.get('level')?.setValue(data.level)
        this.form.get('dateBirth')?.setValue(data.date_birth)
        this.form.get('placeBirth')?.setValue(data.place_birth)
        this.form.get('sex')?.setValue(data.sex)
        this.form.get('dateCin')?.setValue(data.date_cin)
        this.form.get('placeCin')?.setValue(data.place_cin)
        this.form.get('numCin')?.setValue(data.num_cin)
        this.form.get('sex')?.setValue(data.sex)
        this.form.get('dateCin')?.setValue(data.date_cin)
        this.form.get('placeCin')?.setValue(data.place_cin)
        this.form.get('baccYear')?.setValue(data.baccalaureate_years)
        this.form.get('nation')?.setValue(data.nation)
}
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

    makeRandom(lengtOfCode: number): string{
      let text = "";
      let possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
      for(let i = 0; i<lengtOfCode; i++){
        text += possible.charAt(Math.floor(Math.random()*possible.length))
      }
      return text
    }

    

  }

