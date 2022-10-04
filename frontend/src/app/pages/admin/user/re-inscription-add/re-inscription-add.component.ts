import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { typeEtudiant, typeSex, typeNation } from '@app/data/data';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { Droit } from '@app/models/droit';
import { Receipt } from '@app/models/receipt';
import { UserService } from '../user.service';
import { Router } from '@angular/router';
import { AncienStudent } from '@app/models/student';
const BASE_URL = environment.authApiURL;
@Component({
  selector: 'app-re-inscription-add',
  templateUrl: './re-inscription-add.component.html',
  styleUrls: ['./re-inscription-add.component.less']
})
export class ReInscriptionAddComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })


  licence = [{label:"S1", value:"S1", checked:false, disabled:false}, {label:"S2", value:"S2",checked:false, disabled:false}, 
                 {label:"S3", value:"S3",checked:false, disabled:false},{label:"S4", value:"S4",checked:false, disabled:false}, 
                 {label:"S5", value:"S5",checked:false, disabled:false},{label:"S6", value:"S6",checked:false, disabled:false}]

  master_1 = [{label:"S7", value:"S7",checked:false, disabled:false}, {label:"S8", value:"S8",checked:false, disabled:false}] 
  master_2 = [{label:"S9", value:"S9",checked:false, disabled:false}, {label:"S10", value:"S10",checked:false, disabled:false}] 
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
  typeEtudiant = typeEtudiant
  typeNation = typeNation
  options = {
    headers: this.headers
  }
  defaultValue = {
      licence: this.licence,
      master1: this.master_1, 
      master2: this.master_2,
      mention:"54928ac0-af4f-419e-abc0-09fd3a400597",
      journey:"6b877d4c-dd5b-4efa-9a2e-3871027067e8",
      numCarte: this.makeRandom(8),
      firstName: this.makeRandom(12),
      lastName: this.makeRandom(20),
      address: this.makeRandom(30),
      nation: "Malagasy",
      dateBirth: "1995-10-07",
      placeBirth:this.makeRandom(8),
      sex: "Masculin",
      mean: 10,
      baccYear: "2020",
      type: "Passant",

  }
  setDefaultValueForm: () => void;
  blob = new Blob(["assets/images/profil.png"])
  uploadedImage: File = new File([this.blob], 'profile.png');

  constructor(private http: HttpClient, private modal: NzModalService, private fb: FormBuilder, private service: UserService, 
    public router: Router ) {

    this.form = this.fb.group({
      licence: [this.licence, [Validators.required]],
      master1: [this.master_1, [Validators.required]],
      master2: [this.master_2, [Validators.required]],
      mention: [null, [Validators.required]],
      journey: [null, [Validators.required]],
      numCarte: [null, [Validators.required]],
      firstName: [null],
      lastName: [null, [Validators.required]],
      address: [null, [Validators.required]],
      nation: [null, [Validators.required]],
      dateBirth: [null, [Validators.required]],
      placeBirth: [null, [Validators.required]],
      sex: [null, [Validators.required]],
      numCin: [null],
      dateCin: [null],
      placeCin: [null],
      mean: [null, [Validators.required]],
      receipt: [null, [Validators.required]],
      baccYear: [null, [Validators.required]],
      type: [null, [Validators.required]],
      infSemester: [null, [Validators.required]],
      supSemester: [null, [Validators.required]],
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
    const numCarte = localStorage.getItem('numCarte')
    if(numCarte && numCarte.length>0){
      this.isEdit = true
      this.http.get<AncienStudent>(`${BASE_URL}/student/num_carte?num_carte=`+localStorage.getItem("numCarte"), options).subscribe(
        data =>{ 
          this.form.get('numCarte')?.setValue(data.num_carte)
          this.form.get('mention')?.setValue(data.mention)
          this.form.get('journey')?.setValue(data.journey.uuid)
          this.form.get('firstName')?.setValue(data.first_name)
          this.form.get('lastName')?.setValue(data.last_name)
          this.form.get('address')?.setValue(data.address)
          this.form.get('infSemester')?.setValue(data.inf_semester)
          this.form.get('supSemester')?.setValue(data.sup_semester)
          this.form.get('dateBirth')?.setValue(data.date_birth)
          this.form.get('placeBirth')?.setValue(data.place_birth)
          this.form.get('sex')?.setValue(data.sex)
          this.form.get('dateCin')?.setValue(data.date_cin)
          this.form.get('placeCin')?.setValue(data.place_cin)
          this.form.get('numCin')?.setValue(data.num_cin)
          this.form.get('sex')?.setValue(data.sex)
          this.form.get('dateCin')?.setValue(data.date_cin)
          this.form.get('placeCin')?.setValue(data.place_cin)
          this.form.get('mean')?.setValue(data.mean)
          this.form.get('baccYear')?.setValue(data.baccalaureate_years)
          this.form.get('type')?.setValue(data.type)
          this.form.get('nation')?.setValue(data.nation)
          this.form.get('receipt')?.setValue(data.receipt.num)
          this.formDialog.get('numReceipt')?.setValue(data.receipt.num)
          this.formDialog.get('dateReceipt')?.setValue(data.receipt.date)
          this.formDialog.get('priceRigth')?.setValue(data.receipt.price)
          this.url = `${BASE_URL}/student/photo?name_file=`+data.photo
          console.error(data.receipt)
        },
        error => console.error("error as ", error)
      );
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

  showConfirm(name?: string, uuid?: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/mentions/?uuid=`+uuid, this.options).subscribe(
          data => this.all_year = data,
          error => console.error("error as ", error)
        );
      }
    })
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
              num_carte: this.form.value.numCarte,
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
              inf_semester: this.form.value.infSemester,
              sup_semester: this.form.value.supSemester
            }
            console.error(body)
              this.http.post<any>(`${BASE_URL}/student/ancien`,body, this.options).subscribe(
                data => {
                  this.all_year = data,
                  this.router.navigate(['/user/reinscription'])},
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


  handleCancel(): void{
    this.isvisible = false
  }



  handleOk(): void{
    setTimeout(() => {
      this.isvisible = false
      this.isConfirmLoading = false
    }, 3000);
  }

  checkLicence(): void{
    let nbr_check: number = 1
    let indexCheck1: number = -1
    let indexCheck2: number = -1
      if(this.licence[0].checked || this.licence[1].checked || this.licence[2].checked ||
         this.licence[3].checked || this.licence[4].checked || this.licence[5].checked){
        for (let j=0; j<2; j++){
          this.master_1[j].disabled=true
          this.master_2[j].disabled=true
        }
      }else{
        for (let j=0; j<2; j++){
          this.master_1[j].disabled=false
          this.master_2[j].disabled=false
        }
      }
      for (let k=0; k<6; k++){
        if(this.licence[k].checked){
          if(indexCheck1 == -1){
            indexCheck1 = k+1
          }else{
            indexCheck2 = k+1
          }
          nbr_check += 1
        }else{
          nbr_check -= 1
        }
      }
      if(nbr_check == -1){
        for (let k=0; k<6; k++){
          if(this.licence[k].checked){
            this.licence[k].disabled = false
          }else{
            this.licence[k].disabled = true
          }
        }
      }else{
        for (let k=0; k<6; k++){
            this.licence[k].disabled = false
        }
      }
      this.validation(indexCheck1, indexCheck2)
      let check = false
      for(let k=0; k<6; k++){
        if(this.licence[k].checked ){
          check = true
        }
      }
      console.error(check)
      if(check){
        this.form.get('supSemester')?.clearValidators()
        this.form.get('infSemester')?.clearValidators()
      }else{
        this.form.get('supSemester')?.setValidators(Validators.required)
        this.form.get('infSemester')?.setValidators(Validators.required)
      }
  }
  
  validation(indexCheck1: number, indexCheck2: number): void{
    if(indexCheck1 != -1){
      this.form.get('infSemester')?.setValue('S'+indexCheck1)
    }else{
      this.form.get('infSemester')?.reset()
    }
    if(indexCheck2 != -1){
      this.form.get('supSemester')?.setValue('S'+indexCheck2)
    }else{
      this.form.get('supSemester')?.reset()
    }
    console.error("Sup"+this.form.get('supSemester')?.value, "Inf"+this.form.get('infSemester')?.value)
  }
  checkMasterOne(): void{
      if(this.master_1[0].checked || this.master_1[1].checked ){
        for (let j=0; j<2; j++){
          this.master_2[j].disabled=true
        }for (let j=0; j<6; j++){
          this.licence[j].disabled=true
        }
      }else{
        for (let j=0; j<2; j++){
          this.master_2[j].disabled=false
        }for (let j=0; j<6; j++){
          this.licence[j].disabled=false
        }
      }
    }
    checkMasterTwo(): void{
      if(this.master_2[0].checked || this.master_2[1].checked ){
        for (let j=0; j<2; j++){
          this.master_1[j].disabled=true
        }for (let j=0; j<6; j++){
          this.licence[j].disabled=true
        }
      }else{
        for (let j=0; j<2; j++){
          this.master_1[j].disabled=false
        }for (let j=0; j<6; j++){
          this.licence[j].disabled=false
        }
      }
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

