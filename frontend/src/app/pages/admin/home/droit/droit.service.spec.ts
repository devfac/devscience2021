import { TestBed } from '@angular/core/testing';

import { DroitService } from './droit.service';

describe('DroitService', () => {
  let service: DroitService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DroitService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
