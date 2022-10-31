import { TestBed } from '@angular/core/testing';

import { CollegeYearService } from './college-year.service';

describe('CollegeYearService', () => {
  let service: CollegeYearService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CollegeYearService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
