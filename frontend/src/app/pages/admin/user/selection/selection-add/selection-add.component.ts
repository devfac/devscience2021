import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { typeSex, typeEtudiant, typeNation, typeLevel } from '@app/data/data';
import { CollegeYear } from '@app/models/collegeYear';
import { Mention } from '@app/models/mention';
import { MentionService } from '@app/pages/admin/home/mention/mention.service';
import { NzModalRef } from 'ng-zorro-antd/modal';
import { UserService } from '../../user.service';
import { SelectionService } from '../selection.service';

const CODE = "selection"

@Component({
  selector: 'app-selection-add',
  templateUrl: './selection-add.component.html',
  styleUrls: ['./selection-add.component.less']
})
export class SelectionAddComponent implements OnInit {


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
  isReady: boolean = false
  keyMention = CODE+"mention"
  keyYear = CODE+"collegeYear"
  keyNum = CODE+"numSelect"

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

  constructor(
    private fb: FormBuilder, 
    private service: UserService, 
    private selectionService: SelectionService,
    private serviceMention: MentionService, 
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

  async ngOnInit() {

    const numSelect = localStorage.getItem(this.keyNum)
    const year = localStorage.getItem(this.keyYear)

    let uuidMention = localStorage.getItem(this.keyMention)
    if (uuidMention !== null){
      this.allMention.push(await this.serviceMention.getData(uuidMention).toPromise())
      this.isReady = true
    }

    if(numSelect && numSelect.length>0 && year){
      this.isEdit = true
      let  data = await this.selectionService.getStudentByNumSelect(numSelect, year).toPromise()
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
      if (data.num_carte){
        this.isInscrit = true
      }
    }
  }
  
  async submitForm() {
    if (this.form.valid) {
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
          enter_years: localStorage.getItem(this.keyYear),
          num_select: this.form.value.numSelect,
          is_selected: this.form.value.isSelected,
          level: this.form.value.level,
          telephone: this.form.value.phone,
        }
        let year = localStorage.getItem(this.keyYear)
        if (year){
          await this.selectionService.addData(body, year).toPromise()
        }
        this.router.navigate(['/user/selection'])
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

