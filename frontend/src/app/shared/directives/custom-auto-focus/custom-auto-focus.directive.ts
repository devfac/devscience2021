import { AfterViewInit, Directive, ElementRef } from '@angular/core';

@Directive({
  selector: '[appCustomAutoFocus]',
})
export class CustomAutoFocusDirective implements AfterViewInit {
  constructor(private el: ElementRef) {}

  ngAfterViewInit() {
    setTimeout(() => {
      this.el.nativeElement.focus();
    }, 50);
  }
}
