import { Directive, ElementRef, Input, OnInit } from '@angular/core';
import { INotificationType } from '@app/models';

@Directive({
  selector: '[appNotificationStatus]'
})
export class NotificationStatusDirective implements OnInit {
  @Input() type: INotificationType = INotificationType.INFO;

  constructor(private el: ElementRef) {
  }

  ngOnInit(): void {
    switch(this.type) {
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
        this.setColor('red');
        break;
      default:
        this.setColor('black');
        break;
    }
  }

  setColor(color: string) {
    this.el.nativeElement.style.color = color;
  }
}
