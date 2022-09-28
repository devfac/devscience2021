import { TemplateRef } from "@angular/core";

export enum INotificationType {
  SUCCESS, INFO, WARNING, CRITICAL
}

export interface INotification {
  id?: string;
  title?: string;
  content?: string;
  date?: string;
  readed?: boolean,
  template?: TemplateRef<any>;
  type?: INotificationType;
  archive?: boolean;
  modalVisible?: boolean;
}
