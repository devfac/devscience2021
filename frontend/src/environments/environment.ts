// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  authApiURL: 'http://192.168.88.34/api/v1',
  notificationApiURL: 'http://localhost:3000',
  socketApiURL: "ws://192.168.88.34/api/v1/utils/ws/",
  onlineAPI:'http://localhost:8988/api',
  externalApi:"http://localhost:8988/api",
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.
