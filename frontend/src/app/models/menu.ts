export interface Menu {
    id?: number;
    title: string;
    route: string;
    fragment?: string;
    selected?: string | RegExp;
    children?: Menu[];
    open?: boolean;
    icon?: string;
  }
  