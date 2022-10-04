import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfilDropdownComponent } from './profil-dropdown.component';

describe('ProfilDropdownComponent', () => {
  let component: ProfilDropdownComponent;
  let fixture: ComponentFixture<ProfilDropdownComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfilDropdownComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfilDropdownComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
