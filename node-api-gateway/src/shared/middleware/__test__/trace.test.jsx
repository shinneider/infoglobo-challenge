import 'babel-polyfill';
import Request from 'supertest';
import app from '../../../app';

import { TraceMiddleware } from '../trace';

describe('TraceMiddleware test', () => {
  const agent = Request.agent(app);
  const next = jest.fn();
  let req;
  let res;

  beforeEach(() => {
    req = {
      cookies: {},
      headers: {}
    };
    res = {
      cookie: (key, value) => {
        req.cookies[key] = value;
      }
    };
    next.mockReset();
  });

  function validateUuidV4(uuid) {
    let re = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$/;
    return uuid.match(re).length == 1;
  }

  test('Test if TraceMiddleware set IdLog in Cookie', async () => {
    let response = await agent.get('/').expect(200);
    let cookie = response.res.headers['set-cookie'][0];

    let idReqPresent = cookie.startsWith('idLog');
    expect(idReqPresent).toBe(true);

    let uuid = cookie.substr(6, 36);
    expect(validateUuidV4(uuid)).toBe(true);
  });

  test('Test if TraceMiddleware get IdLog in cookie', async () => {
    req.cookies.idLog = '80c1e153-0d41-4ca6-8580-5956e4b6232f';
    TraceMiddleware(req, res, next);
    expect(req.headers.idLog).toEqual('80c1e153-0d41-4ca6-8580-5956e4b6232f');
  });

  test('Test if TraceMiddleware set IdLog in header', async () => {
    TraceMiddleware(req, res, next);
    expect(validateUuidV4(req.headers.idLog)).toBe(true);
  });

  test('Test if TraceMiddleware set unique IdLog per browser', async () => {
    TraceMiddleware(req, res, next);
    let firstRequestId = req.headers.IdLog;

    req.headers = {};
    TraceMiddleware(req, res, next);
    let SecondRequestId = req.headers.IdLog;

    expect(firstRequestId).toEqual(SecondRequestId);
  });

  test('Test if TraceMiddleware get idReq in header', async () => {
    req.headers.idReq = '80c1e153-0d41-4ca6-8580-5956e4b6232f';
    TraceMiddleware(req, res, next);
    expect(req.headers.idReq).toEqual('80c1e153-0d41-4ca6-8580-5956e4b6232f');
  });

  test('Test if TraceMiddleware set idReq in header', async () => {
    TraceMiddleware(req, res, next);
    expect(validateUuidV4(req.headers.idReq)).toBe(true);
  });

  test('Test if TraceMiddleware set unique idReq per request', async () => {
    TraceMiddleware(req, res, next);
    let firstRequestId = req.headers.idReq;

    req.headers = {};
    TraceMiddleware(req, res, next);
    let SecondRequestId = req.headers.idReq;

    expect(firstRequestId).not.toEqual(SecondRequestId);
  });
});
