import { TestBed } from '@angular/core/testing';

import { ReInscriptionService } from './re-inscription.service';

describe('ReInscriptionService', () => {
  let service: ReInscriptionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ReInscriptionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
