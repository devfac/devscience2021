import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BaccSerieComponent } from './bacc-serie.component';

describe('BaccSerieComponent', () => {
  let component: BaccSerieComponent;
  let fixture: ComponentFixture<BaccSerieComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BaccSerieComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BaccSerieComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
