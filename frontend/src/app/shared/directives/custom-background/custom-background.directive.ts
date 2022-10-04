import { Directive, ElementRef, HostListener, Input, OnInit } from '@angular/core';
import { INotificationType } from '@app/models';

@Directive({
  selector: '[appCustomBackground]',
})
export class CustomBackgroundDirective implements OnInit {
  @Input() type: INotificationType = INotificationType.INFO;
  color = '';

  constructor(private el: ElementRef) {}

  ngOnInit(): void {
    switch (this.type) {
      case INotificationType.INFO:
        this.setColor('#1890ff');
        break;
      case INotificationType.SUCCESS:
        this.setColor('#52c41a');
        break;
      case INotificationType.WARNING:
        this.setColor('#FFD204');
        break;
      case INotificationType.CRITICAL:
        this.setColor('#FF0000');
        break;
      default:
        this.setColor('#000000');
        break;
    }
  }

  @HostListener('mousedown')
  onMouseDown() {
    const activeColor = `${this.color}20`;
    this.el.nativeElement.style.backgroundColor = activeColor;
  }

  @HostListener('mouseup')
  onMouseUp() {
    const hoverColor = `${this.color}15`;
    this.el.nativeElement.style.backgroundColor = hoverColor;
  }

  @HostListener('mouseover')
  onMouseOver() {
    const hoverColor = `${this.color}15`;
    this.el.nativeElement.style.backgroundColor = hoverColor;
  }

  @HostListener('mouseout')
  onMouseOut() {
    const bgColor = `${this.color}10`;
    this.el.nativeElement.style.backgroundColor = bgColor;
  }

  setColor(color: string) {
    this.color = color;
    const bgColor = `${this.color}10`;
    this.el.nativeElement.style.backgroundColor = bgColor;
  }
}
