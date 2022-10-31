import { HttpParams } from '@angular/common/http';
import { otherQueryParams, QueryParams } from '@app/models/query';

export function parseQueryParams(params?: QueryParams, othserParams?: otherQueryParams ,defaultOrder?: string): HttpParams {
  if (params) {
    const { pageIndex, pageSize, sortField, sortOrder} = params;
    const limit = pageSize;
    const offset = pageSize * (pageIndex - 1);

    const order =
      sortOrder !== null ? (sortOrder === 'ascend' ? 'ASC' : 'DESC') : defaultOrder || null;
    const orderBy = sortField;

    let _params = new HttpParams().append('limit', limit).append('offset', offset);

    if (order) _params = _params.append('order', order);
    if (orderBy) _params = _params.append('order_by', orderBy);

    if (othserParams) {
      for (const [key, value] of Object.entries(othserParams)){
        console.log(key, value)
        _params = _params.append(key, value);
      }
  }
    return _params;
  } else return new HttpParams();
}
