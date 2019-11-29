import { v4 } from 'uuid';

export function TraceMiddleware(req, res, next) {
  if (req.cookies['idLog']) {
    req.headers['idLog'] = req.cookies['idLog'];
  } else {
    req.headers['idLog'] = v4();
    res.cookie('idLog', req.headers['idLog']);
  }

  if (!req.headers['idReq']) {
    req.headers['idReq'] = v4();
  }

  next();
}
