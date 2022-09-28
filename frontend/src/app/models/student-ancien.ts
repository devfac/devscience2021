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
    price_sigth: number,
    type: string,
    photo: string,
    num_receipt: Array<string>
    date_receipt: Array<string>
    journey: Journey,
    receipt: Receipt
}