import { Journey } from "./journey";
import { NzTableFilterFn, NzTableFilterList, NzTableSortFn, NzTableSortOrder } from "ng-zorro-antd/table";

export interface Ec{
    uuid: string,
    title: string,
    semester: string
    journey: Journey,
    value_ue: string,
    weight: number,
    user: string,
    is_optional: boolean
    abbreviation_journey: string,
}

export interface EcColumn{
    title: string;
    abbreviation_journey: string,
    semester: string,
    weight: string,
    value_ue: string,
    action:string,
}

export interface ColumnItem{
    name: string;
    sortOrder: NzTableSortOrder | null;
    sortFn: NzTableSortFn<EcColumn> | null;
    listOfFilter: NzTableFilterList;
    filterFn: NzTableFilterFn<EcColumn> | null;
    filterMultiple: boolean;
    sortDirections: NzTableSortOrder[];
}