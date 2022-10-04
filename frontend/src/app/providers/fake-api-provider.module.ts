import { HTTP_INTERCEPTORS } from "@angular/common/http";
import { FakeApiInterceptor } from "@app/helpers";

export const fakeApiProvider = {
  // use fake api in place of Http service for backend-less development
  provide: HTTP_INTERCEPTORS,
  useClass: FakeApiInterceptor,
  multi: true
};