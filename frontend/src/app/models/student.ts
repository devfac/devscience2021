import { NzTableSortOrder, NzTableSortFn, NzTableFilterList, NzTableFilterFn } from "ng-zorro-antd/table"
import { Journey } from "./journey"
import { Receipt } from "./receipt"

export interface AncienStudent{
    uuid: string,
    last_name: string,
    first_name: string,
    date_birth: Date,
    place_birth: string,
    address: string,
    sex: string,
    nation: string,
    num_cin: string,
    date_cin: Date,
    place_cin: string,
    mention: string,
    actual_years: string,
    num_carte: string,
    num_baccalaureat: string,
    baccalaureate_years: string,
    mean: number,
    inf_semester: string,
    sup_semester: string,
    price_rigth: number,
    type: string,
    photo: string,
    num_receipt: Array<string>
    date_receipt: Array<string>
    journey: Journey,
    receipt: Receipt

    num_select: string,
    is_selected: false,
    enter_years: string,

    situation: string,
    telephone: string,
    baccalaureate_num: string,
    baccalaureate_center: string,
    baccalaureate_series: string,
    work: string,
    father_name: string,
    father_work: string,
    mother_name: string,
    mother_work: string,
    parent_address: string,
    uuid_mention: string,
    level: string,
}

export interface StudentColumn{
    title: string;
    last_name: string,
    inf_semester: string,
    sup_semester: string,
    journey: Journey,
    is_selected: false,
    level: string,
}

export interface StudentInfo{
    info: any;
    Normal: any,
    Rattrapage: any,
}

export interface ColumnItem{
    name: string;
    sortOrder: NzTableSortOrder | null;
    sortFn: NzTableSortFn<StudentColumn> | null;
    listOfFilter: NzTableFilterList;
    filterFn: NzTableFilterFn<StudentColumn> | null;
    filterMultiple: boolean;
    sortDirections: NzTableSortOrder[];
}