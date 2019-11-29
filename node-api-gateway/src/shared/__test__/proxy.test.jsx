import 'babel-polyfill';

import { proxyConfig } from '../proxy';

describe('Routers test', () => {
  let req

  beforeEach(() => {
    req = {
      url: '/sample-url'
    }
  });

  test('Contains PATH_PREFIX', async () => {
    process.env.PATH_PREFIX = ''
    const response = proxyConfig.proxyReqPathResolver(req)
    expect(response).toEqual(req.url);
  });

  test('No contains PATH_PREFIX', async () => {
    process.env.PATH_PREFIX = '/test'
    const response = proxyConfig.proxyReqPathResolver(req)
    expect(response).toEqual('/test' + req.url);
  });

});
