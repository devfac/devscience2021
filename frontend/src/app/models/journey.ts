import { NzTableSortOrder, NzTableSortFn, NzTableFilterList, NzTableFilterFn } from "ng-zorro-antd/table";

export interface Journey{
    uuid: string,
    title: string,
    semester: string,
    abbreviation: string,
    mention: any
    mention_title: string
}


export interface JourneyColumn{
    title: string;
    abbreviation: string,
    mention_title: string
}

export interface ColumnItem{
    name: string;
    sortOrder: NzTableSortOrder | null;
    sortFn: NzTableSortFn<JourneyColumn> | null;
    listOfFilter: NzTableFilterList;
    filterFn: NzTableFilterFn<JourneyColumn> | null;
    filterMultiple: boolean;
    sortDirections: NzTableSortOrder[];
}