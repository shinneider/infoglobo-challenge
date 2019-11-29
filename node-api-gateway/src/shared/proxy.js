import { outputLogger } from './middleware/logger';

export const proxyConfig = {
  proxyReqPathResolver: function(req) {
    /*
      this functions append a prefix in a url without change 
      the API GATEWAY url.

      Ex -> aws lambda all endpoints contains stage prefix in urls
            https://aws-url/STAGE-PREFIX/your-app-urls

      without this occurrs a erro in this case, because `httpProxy` lib
      try to redirect the API GATEWAY to url containing a prefix.
    */
    if (process.env.PATH_PREFIX) {
      return process.env.PATH_PREFIX + req.url;
    }

    return req.url;
  },
  userResDecorator: function(proxyRes, proxyResData, userReq, userRes) {
    outputLogger(userReq, proxyRes, proxyResData);
    return proxyResData;
  }
};
