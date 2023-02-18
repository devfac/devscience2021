import { TestBed } from '@angular/core/testing';

import { BaccSerieService } from './bacc-serie.service';

describe('BaccSerieService', () => {
  let service: BaccSerieService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BaccSerieService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
