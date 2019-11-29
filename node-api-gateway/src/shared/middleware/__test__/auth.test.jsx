import 'babel-polyfill';
import Request from 'supertest';
import app from '../../../app';

import { AuthMiddleware } from '../auth';

describe('AuthMiddleware test', () => {
  const agent = Request.agent(app);
  const next = jest.fn();
  let req;
  let res;

  beforeEach(() => {
    req = {headers: {}};
    res = {};
    next.mockReset();
  });

  test('No contains JWT token', async () => {
    AuthMiddleware(req, res, next);
    expect(req.headers.auth).toBe(false);
    expect(req.headers.userId).toBe(null);
  });

  test('Contains valid jwt token', async () => {
    req.headers.authorization = 'jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0'
                               +'b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTY4NDgzM'
                               +'zg4LCJqdGkiOiI1ZjMwNWRhOWVhYjk0ODBkYjAxOWEwOT'
                               +'ZhYjYyOTg4MiIsInVzZXJfaWQiOjF9.-om62aoHPLO_O8'
                               +'O_if6C5aFqlZDUJWs9SXFjNTPngkA","key":"auth_to'
                               +'ken","enabled":true,"sessionValue":"eyJ0eXAiO'
                               +'iJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlI'
                               +'joiYWNjZXNzIiwiZXhwIjoxNTY4NDgzMzg4LCJqdGkiOi'
                               +'I1ZjMwNWRhOWVhYjk0ODBkYjAxOWEwOTZhYjYyOTg4MiI'
                               +'sInVzZXJfaWQiOjF9.-om62aoHPLO_O8O_if6C5aFqlZD'
                               +'UJWs9SXFjNTPngkA';

    AuthMiddleware(req, res, next);
    expect(req.headers.auth).toBe(true);
    expect(req.headers.userId).toBe(1);
  });

  test('Contains invalid jwt token', async () => {
    await agent.get('/').set('authorization', 'jwt ').expect(401);
  });

});
