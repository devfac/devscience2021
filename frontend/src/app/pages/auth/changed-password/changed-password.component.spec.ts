import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChangedPasswordComponent } from './changed-password.component';

describe('ChangedPasswordComponent', () => {
  let component: ChangedPasswordComponent;
  let fixture: ComponentFixture<ChangedPasswordComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ChangedPasswordComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChangedPasswordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
