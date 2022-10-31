import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { typeSex, typeEtudiant, typeNation, typeLevel } from '@app/data/data';
import { CollegeYear } from '@app/models/collegeYear';
import { Droit } from '@app/models/droit';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { Receipt } from '@app/models/receipt';
import { AncienStudent } from '@app/models/student';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { UserService } from '../../user.service';

const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-selection-add',
  templateUrl: './selection-add.component.html',
  styleUrls: ['./selection-add.component.less']
})
export class SelectionAddComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })


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
  typeSex = typeSex
  typeEtudiant = typeEtudiant
  typeNation = typeNation
  typeLevel = typeLevel
  isInscrit: boolean = false
  options = {
    headers: this.headers
  }
  defaultValue = {
      mention:"54928ac0-af4f-419e-abc0-09fd3a400597",
      numSelect: this.makeRandomNum(),
      firstName: this.makeRandom(12),
      lastName: this.makeRandom(20),
      address: this.makeRandom(30),
      nation: "Malagasy",
      dateBirth: "1995-10-07",
      placeBirth:this.makeRandom(8),
      sex: "Masculin",
      isSelected: false,
      level: 'L1',
      phone: '034 88 763 04'

  }
  setDefaultValueForm: () => void;

  constructor(private http: HttpClient, private modal: NzModalService, private fb: FormBuilder, private service: UserService, 
    public router: Router ) {

    this.form = this.fb.group({
      mention: [null, [Validators.required]],
      numSelect: [null, [Validators.required]],
      firstName: [null],
      lastName: [null, [Validators.required]],
      address: [null, [Validators.required]],
      nation: [null, [Validators.required]],
      dateBirth: [null, [Validators.required]],
      placeBirth: [null, [Validators.required]],
      sex: [null, [Validators.required]],
      level: [null, [Validators.required]],
      phone: [null],
      numCin: [null],
      dateCin: [null],
      placeCin: [null],
      isSelected: [false],
    });

    this.setDefaultValueForm = () => this.service.setDefaultValueForm(this.form, this.defaultValue);

   }

  ngOnInit(): void {
    let options = {
      headers: this.headers
    }
    this.http.get<Mention>(`${BASE_URL}/mentions/`+localStorage.getItem("uuid_mention"), options).subscribe(
      data =>{ 
        this.allMention.push(data),
        this.form.get("mention")?.setValue(data.uuid)
      },
      error => console.error("error as ", error)
    );

    const numSelect = localStorage.getItem('numSelect')
    if(numSelect && numSelect.length>0){
      this.isEdit = true
      this.http.get<AncienStudent>(`${BASE_URL}/student/new?num_select=`+localStorage.getItem("numSelect"), options).subscribe(
        data =>{ 
          console.log(data)
          this.form.get('numSelect')?.setValue(data.num_select)
          this.form.get('mention')?.setValue(data.uuid_mention)
          this.form.get('firstName')?.setValue(data.first_name)
          this.form.get('lastName')?.setValue(data.last_name)
          this.form.get('address')?.setValue(data.address)
          this.form.get('dateBirth')?.setValue(data.date_birth)
          this.form.get('placeBirth')?.setValue(data.place_birth)
          this.form.get('dateCin')?.setValue(data.date_cin)
          this.form.get('placeCin')?.setValue(data.place_cin)
          this.form.get('numCin')?.setValue(data.num_cin)
          this.form.get('sex')?.setValue(data.sex)
          this.form.get('dateCin')?.setValue(data.date_cin)
          this.form.get('placeCin')?.setValue(data.place_cin)
          this.form.get('nation')?.setValue(data.nation)
          this.form.get('isSelected')?.setValue(data.is_selected)
          this.form.get('level')?.setValue(data.level)
          this.form.get('phone')?.setValue(data.telephone)
          if (data.num_carte.length > 0){
            this.isInscrit = true
            console.log(data.num_carte)
            console.log(this.isInscrit)
          }
        },
        error => console.error("error as ", error)
      );
    }
  }
  
  submitForm(): void {
    if (this.form.valid) {
      const title = this.form.value.title
      const mean = this.form.value.mean
      this.isConfirmLoading = true
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
          enter_years: localStorage.getItem('college_years'),
          num_select: this.form.value.numSelect,
          is_selected: this.form.value.isSelected,
          level: this.form.value.level,
          telephone: this.form.value.phone,
        }
        console.error(body)
          this.http.post<any>(`${BASE_URL}/student/new`,body, this.options).subscribe(
            data => {
              this.allYear = data,
              this.router.navigate(['/user/selection'])},
            error => console.error("error as ", error)
          )
      
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

    makeRandomNum(): number{
      return Math.floor((Math.random()*1001)+1)
    }

    

  }

