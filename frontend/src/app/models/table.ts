import { TemplateRef } from '@angular/core';
import { NgStyleInterface } from 'ng-zorro-antd/core/types';

export enum TableHeaderType {
  NORMAL,
  ACTION,
}

export interface TableHeader {
  title: string;
  selector: string; // nullable for action type
  style?: NgStyleInterface;
  width?: string; // nullable
  hidden?: boolean; // default true
  type?: TableHeaderType; // default NORMAL
  isSortable?: boolean; // default true
  sortOrder?: any; // should not be defined manually
  template?: TemplateRef<any>; // nullable
  formatter?: (value: any) => string; // nullable
  colspan?: number
  rowspan?: number
  btnType?: boolean
  editable?: boolean
}

export interface TableActions {
  add?: boolean;
  edit?: boolean;
  delete?: boolean;
  detail?: boolean;
  restore?: boolean
}
