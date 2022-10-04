import { ElementRef } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { NotificationStatusDirective } from './notification-status.directive';

describe('NotificationStatusDirective', () => {
  let directive: NotificationStatusDirective;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [ElementRef] });
    directive = TestBed.inject(NotificationStatusDirective);
  });

  it('should create an instance', () => {
    expect(directive).toBeTruthy();
  });
});
