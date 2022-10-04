import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { Router } from '@angular/router';
// import { INotificationType, User } from '@app/models';
// import { NotificationService } from '@app/services/notification/notification.service';
import { AuthService } from '@app/services/auth/auth.service';
import { first } from 'rxjs/operators';
import { NzMessageService } from 'ng-zorro-antd/message';
import { User } from '@app/models';

@Component({
  selector: 'app-edit-password',
  templateUrl: './edit-password.component.html',
  styleUrls: ['./edit-password.component.less'],
})
export class EditPasswordComponent implements OnInit {
  @ViewChild('notification', { static: false }) notificationTemplate?: TemplateRef<{}>;
  form!: FormGroup;
  loading = false;
  user: User | null = null;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService,
    private message: NzMessageService,
  ) {
    this.authService.user.subscribe(_user => {
      this.user = _user;
    })
  }

  ngOnInit(): void {
    this.form = this.fb.group({
      old_password: [null, [Validators.required]],
      new_password: [null, [Validators.required, Validators.minLength(8), Validators.pattern(/[A-Z]/), Validators.pattern(/[a-z]/), Validators.pattern(/[0-9]/)]],
      confirm_password: [null, [Validators.required, this.confirmPassword]],
    });
  }

  confirmPassword: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
    const new_password = this?.form?.get('new_password')?.value;
    const confirm_password = control.value;
    return new_password === confirm_password ? null : { mismatch: true };
  }

  submitForm(): void {
    if (this.form.valid && this.user) {
      this.loading = true;
      const old_password = this.form.value.old_password
      const password = this.form.value.new_password
      const value = {
        ...this.user,
        password: this.form.value.new_password,
        old_password: this.form.value.old_password
      };
      this.authService.update(password, old_password)
        .pipe(first())
        .subscribe({
          next: () => {
            this.authService.logout();
            this.router.navigate(["/auth/login"]);
          },
          error: error => {
            this.message.error(error);
            this.loading = false;
          }
        });
    } else {
      Object.values(this.form.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
    }
  }
}
