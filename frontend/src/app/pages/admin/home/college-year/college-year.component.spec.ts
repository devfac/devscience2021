import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CollegeYearComponent } from './college-year.component';

describe('CollegeYearComponent', () => {
  let component: CollegeYearComponent;
  let fixture: ComponentFixture<CollegeYearComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CollegeYearComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CollegeYearComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
