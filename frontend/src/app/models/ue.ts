import { NzTableSortOrder, NzTableSortFn, NzTableFilterList, NzTableFilterFn } from "ng-zorro-antd/table";
import { Ec } from "./ec";
import { Journey } from "./journey";

export interface Ue{
    uuid: string,
    title: string,
    journey: Journey,
    credit: number,
    semester: string
    value: string
    abbreviation_journey: string,
}

export interface UeEc{
    uuid: string,
    title: string,
    journey: Journey,
    credit: number,
    semester: string
    value: string
    abbreviation_journey: string,
    ec: Ec[]
}

export interface UeColumn{
    title: string;
    semester: string,
    credit: string,
    value: string,
    abbreviation_journey: string,
    action:string,
}

export interface ColumnItem{
    name: string;
    sortOrder: NzTableSortOrder | null;
    sortFn: NzTableSortFn<UeColumn> | null;
    listOfFilter: NzTableFilterList;
    filterFn: NzTableFilterFn<UeColumn> | null;
    filterMultiple: boolean;
    sortDirections: NzTableSortOrder[];
}