import { Injectable } from '@angular/core';
import { HttpRequest, HttpResponse, HttpHandler, HttpEvent, HttpInterceptor, HTTP_INTERCEPTORS } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { delay, materialize, dematerialize } from 'rxjs/operators';
import { User } from '../models';

// array in local storage for registered users
const usersKey = 'fac-science-user-key';
let users = JSON.parse(localStorage.getItem(usersKey) || 'null') || [];

@Injectable()
export class FakeApiInterceptor implements HttpInterceptor {
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const { url, method, headers, body } = request;

    return handleRoute();

    function handleRoute() {
      switch (true) {
        case url.endsWith('/users/authenticate') && method === 'POST':
          return authenticate();
        case url.endsWith('/users/register') && method === 'POST':
          return register();
        case url.endsWith('/users') && method === 'GET':
          return getUsers();
        case url.match(/\/users\/\d+$/) && method === 'GET':
          return getUserById();
        case url.match(/\/users\/\d+$/) && method === 'PUT':
          return updateUser();
        case url.match(/\/users\/\d+$/) && method === 'DELETE':
          return deleteUser();
        default:
          // pass through any requests not handled above
          return next.handle(request);
      }
    }

    // route functions

    function authenticate() {
      const { email, password } = body;
      const user = users.find((_user: User) => _user.email === email && _user.password === password);
      if (!user) return error('Email or password is incorrect');
      return ok({
        ...basicDetails(user),
        token: 'fake-jwt-token'
      });
    }

    function register() {
      const user = body
      if (users.find((_user: User) => _user.email === user.email)) {
        return error('Email "' + user.email + '" is already taken')
      } else {
        user.id = users.length ? Math.max(...users.map((_user: User) => _user.uuid)) + 1 : 1;
        user.updateAt = new Date().toISOString();
        user.createAt = new Date().toISOString();
        users.push(user);
        localStorage.setItem(usersKey, JSON.stringify(users));
        return ok();
      }
    }

    function getUsers() {
      if (!isLoggedIn()) return unauthorized();
      return ok(users.map((_user: User) => basicDetails(_user)));
    }

    function getUserById() {
      if (!isLoggedIn()) return unauthorized();

      const user = users.find((_user: User) => _user.uuid === idFromUrl());
      return ok(basicDetails(user));
    }

    function updateUser() {
      if (!isLoggedIn()) return unauthorized();

      let params = body;
      let user = users.find((_user: User) => _user.uuid === idFromUrl());

      // only update password if entered
      if (!params.password) {
        delete params.password;
      } else {
        if (params.old_password !== user.password) {
          return error("Old password is incorrect");
        }
      }

      // update and save user
      Object.assign(user, params);
      localStorage.setItem(usersKey, JSON.stringify(users));
      return ok();
    }

    function deleteUser() {
      if (!isLoggedIn()) return unauthorized();

      users = users.filter((_user: User) => _user.uuid !== idFromUrl());
      localStorage.setItem(usersKey, JSON.stringify(users));
      return ok();
    }

    // helper functions

    function ok(body?: any) {
      return of(new HttpResponse({ status: 200, body }))
        .pipe(delay(500)); // delay observable to simulate server api call
    }

    function error(message: any) {
      return throwError({ error: { message } })
        .pipe(materialize(), delay(500), dematerialize()); // call materialize and dematerialize to ensure delay even if an error is thrown (https://github.com/Reactive-Extensions/RxJS/issues/648);
    }

    function unauthorized() {
      return throwError({ status: 401, error: { message: 'Unauthorized' } })
        .pipe(materialize(), delay(500), dematerialize());
    }

    function basicDetails(_user: User) {
      const { uuid, email, first_name, last_name, updateAt, createAt } = _user;
      return { uuid, email, first_name, last_name, updateAt, createAt };
    }

    function isLoggedIn() {
      return headers.get('Authorization') === 'Bearer fake-jwt-token';
    }

    function idFromUrl() {
      const urlParts = url.split('/');
      return urlParts[urlParts.length - 1];
    }
  }
}
