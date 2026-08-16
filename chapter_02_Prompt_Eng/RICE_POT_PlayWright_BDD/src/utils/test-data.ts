import { config } from '../support/config';

export interface UserCredentials {
  username: string;
  password: string;
}

export const testData = {
  invalidUser: {
    username: process.env.INVALID_USERNAME ?? 'invalid.user@example.com',
    password: process.env.INVALID_PASSWORD ?? 'InvalidPassword123!',
  },
  get validUser(): UserCredentials {
    return { username: config.username, password: config.password };
  },
};
