import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InscriptionAddComponent } from './inscription-add.component';

describe('InscriptionAddComponent', () => {
  let component: InscriptionAddComponent;
  let fixture: ComponentFixture<InscriptionAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InscriptionAddComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InscriptionAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
