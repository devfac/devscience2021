export interface QueryParams {
  semester?: string | null;
  session?: string | null;
  pageIndex: number,
  pageSize: number,
  sortField: string | null,
  sortOrder: string | null,
}

export interface otherQueryParams {
  uuid_journey?: string | null;
  uuid_mention?: string | null;
  college_year?: string | null;
  num_select?: string | null;
  num_carte?: string | null;
  value_ue?: string | null;
  value_ec?: string | null;
  credit?: string | null;
  mean?: string | null;
  value?: number | null;
  type_?: string | null;
  session?: string | null;
  semester?: string | null;
  level?: string | null;
  title?: string | null;
}
