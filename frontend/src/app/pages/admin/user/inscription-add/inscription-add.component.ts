import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { typeSex, typeEtudiant, typeNation, typeSituation, typeSerie, typeLevel } from '@app/data/data';
import { CollegeYear } from '@app/models/collegeYear';
import { Droit } from '@app/models/droit';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { Receipt } from '@app/models/receipt';
import { AncienStudent } from '@app/models/student';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { UserService } from '../user.service';

const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-inscription-add',
  templateUrl: './inscription-add.component.html',
  styleUrls: ['./inscription-add.component.less']
})
export class InscriptionAddComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  all_year: CollegeYear[] = []
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
  all_mention: Mention[] = []
  all_journey: Journey[] = []
  all_price: Droit[] = []
  all_receipt: Receipt[] = []
  typeSex = typeSex
  typeSituation = typeSituation
  typeNation = typeNation
  typeSerie = typeSerie
  typeLevel = typeLevel
  options = {
    headers: this.headers
  }
  defaultValue = {
      mention:"54928ac0-af4f-419e-abc0-09fd3a400597",
      journey:"6b877d4c-dd5b-4efa-9a2e-3871027067e8",
      numInsc: this.makeRandom(8),
      firstName: this.makeRandom(12),
      lastName: this.makeRandom(20),
      address: this.makeRandom(30),
      nation: "Malagasy",
      dateBirth: "1995-10-07",
      placeBirth:this.makeRandom(8),
      sex: "Masculin",
      baccYear: "2020",
      type: "Passant",
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
      level: "L1",

  }
  setDefaultValueForm: () => void;
  blob = new Blob(["assets/images/profil.png"])
  uploadedImage: File = new File([this.blob], 'profile.png');

  constructor(private http: HttpClient, private modal: NzModalService, private fb: FormBuilder, private service: UserService, 
    public router: Router ) {

    this.form = this.fb.group({
      mention: [null, [Validators.required]],
      journey: [null, [Validators.required]],
      numSelect: [null, [Validators.required]],
      firstName: [null],
      lastName: [null, [Validators.required]],
      address: [null, [Validators.required]],
      nation: [null, [Validators.required]],
      phone: [null, [Validators.required]],
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
      level: [null, [Validators.required]],

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

  ngOnInit(): void {
    let options = {
      headers: this.headers
    }
    const numSelect = localStorage.getItem('numSelect')
    if(numSelect && numSelect.length>0){
      this.isEdit = true
      this.http.get<AncienStudent>(`${BASE_URL}/student/new?num_select=`+numSelect, options).subscribe(
        data =>{ 
          this.form.get('numSelect')?.setValue(data.num_carte)
          this.form.get('mention')?.setValue(data.mention)
          this.form.get('journey')?.setValue(data.journey.uuid)
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
          this.form.get('receipt')?.setValue(data.receipt.num)
          this.formDialog.get('numReceipt')?.setValue(data.receipt.num)
          this.formDialog.get('dateReceipt')?.setValue(data.receipt.date)
          this.formDialog.get('priceRigth')?.setValue(data.receipt.price)

          this.form.get('situation')?.setValue(data.sex)
          this.form.get('telephone')?.setValue(data.sex)
          this.form.get('baccNum')?.setValue(data.sex)
          this.form.get('baccCenter')?.setValue(data.sex)
          this.form.get('baccSeri')?.setValue(data.sex)
          this.form.get('work')?.setValue(data.sex)
          this.form.get('fatherName')?.setValue(data.sex)
          this.form.get('fatherWork')?.setValue(data.sex)
          this.form.get('motherName')?.setValue(data.sex)
          this.form.get('motherWork')?.setValue(data.sex)
          this.form.get('parentAddress')?.setValue(data.sex)
          this.url = `${BASE_URL}/student/photo?name_file=`+data.photo
          console.error(data.receipt)
        },
        error => console.error("error as ", error)
      );
    }else{
      this.isEdit=false
    }

    this.http.get<Mention>(`${BASE_URL}/mentions/`+localStorage.getItem("uuid_mention"), options).subscribe(
      data =>{ 
        this.all_mention.push(data),
        this.form.get("mention")?.setValue(data.uuid)
      },
      error => console.error("error as ", error)
    );

    this.http.get<Journey[]>(`${BASE_URL}/journey/`+localStorage.getItem("uuid_mention"), options).subscribe(
      data =>{ 
        this.all_journey=data
      },
      error => console.error("error as ", error)
    );

    this.http.get<Droit[]>(`${BASE_URL}/droit/by_mention?uuid_mention=`+
      localStorage.getItem("uuid_mention")+'&year='+localStorage.getItem("college_years"), options).subscribe(
      data =>{ 
        this.all_price=data
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
  
  submitForm(): void {
    if (this.form.valid) {
      const title = this.form.value.title
      const mean = this.form.value.mean
      this.isConfirmLoading = true
      
      const formData = new FormData();
      formData.append("uploaded_file", this.uploadedImage)
      this.http.post<any>(`${BASE_URL}/student/upload_photo/?num_carte=`+this.form.value.numCarte,formData, this.options).subscribe(
        data =>{ 
          console.error(data)
          if(data.filename){
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
              type: this.form.value.type,
              photo: data.filename,
              uuid_journey: this.form.value.journey,
              level: this.form.value.level,

              situation: this.form.value.level,
              telephone: this.form.value.telephone,
              baccalaureate_num: this.form.value.baccNum,
              baccalaureate_center: this.form.value.baccCenter,
              baccalaureate_seri: this.form.value.baccSeri,
              work: this.form.value.work,
              father_name: this.form.value.fatherName,
              father_work: this.form.value.fatherWork,
              mother_name: this.form.value.motherName,
              mother_work: this.form.value.motherWork,
              parent_address: this.form.value.parentAddress,

            }
            console.error(body)
              this.http.put<AncienStudent>(`${BASE_URL}/student/new?num_select=`+this.form.value.numSelect,body, this.options).subscribe(
                data => {
                  this.router.navigate(['/user/inscription'])},
                error => console.error("error as ", error)
              )
          }
        },
        error => console.error("error as ", error)
      );

      
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
    this.isvisible = true;
    console.error(this.form.get('receipt')?.value)
    if(!this.form.get('receipt')?.value){

      this.formDialog.reset()
    }
  }

  showModalEdit(uuid: string): void{
    this.isEdit = true
    this.uuid = uuid
    this.http.get<any>(`${BASE_URL}/college_year/`+uuid, this.options).subscribe(
      data => {
        console.error(data)
        this.form.get('title')?.setValue(data.title),
        this.form.get('mean')?.setValue(data.mean)
    },
      error => console.error("error as ", error)
    );
    this.isvisible = true
  }

  getStudentByNumSelect(): void{
    const numSelect = this.form.get('numSelect')?.value
    if(numSelect && numSelect.length>0){
    this.http.get<AncienStudent>(`${BASE_URL}/student/new?num_select=`+numSelect, this.options).subscribe(
      data =>{ 
        console.log(data)
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
  },
  error => console.error("error as ", error)
    )
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

