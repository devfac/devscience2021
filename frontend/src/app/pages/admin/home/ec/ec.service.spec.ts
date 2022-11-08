import { TestBed } from '@angular/core/testing';

import { EcService } from './ec.service';

describe('EcService', () => {
  let service: EcService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EcService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
