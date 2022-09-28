import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReInscriptionAddComponent } from './re-inscription-add.component';

describe('ReInscriptionAddComponent', () => {
  let component: ReInscriptionAddComponent;
  let fixture: ComponentFixture<ReInscriptionAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReInscriptionAddComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ReInscriptionAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
