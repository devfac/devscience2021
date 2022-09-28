import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReInscriptionComponent } from './re-inscription.component';

describe('ReInscriptionComponent', () => {
  let component: ReInscriptionComponent;
  let fixture: ComponentFixture<ReInscriptionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReInscriptionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ReInscriptionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
