
export interface User {
  json(): any;
  uuid: string,
  email: string,
  password: string,
  confirm_password?: string,
  first_name?: string,
  last_name?: string,
  createAt?: string,
  updateAt?: string,
  uuid_role?: string,
  uuid_mention?: any,
  mention?: any,
  is_admin: boolean,
  is_active: boolean,
  is_superuser: boolean,
  access_token: string,
}