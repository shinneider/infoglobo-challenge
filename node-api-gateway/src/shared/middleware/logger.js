import { logger } from '../logger';

export function inputLogger(req) {
  /* TODO: Hidden sensitive fields in req.body data (password, cpf and 
           anothers sensitive fields)
    Suggest create a recursive function and check all field of a body and
    change value of fields named with 'password', 'cpf' or 'email' to
    masked value '*****'.
  */
  logger.info(
    `INPUT - ID LOG: ${req.headers['idLog']} - ID REQ: ${
      req.headers['idReq']
    } - AUTH: ${req.headers['auth']} - USER: ${req.headers['userId']} - URL: ${
      req.url
    } - METHOD: ${req.method} - BODY: ${JSON.stringify(req.body)}`
  );
}

export function outputLogger(req, res, body) {
  logger.info(
    `OUTPUT - ID LOG: ${req.headers['idLog']} - ID REQ: ${
      req.headers['idReq']
    } - STATUS: ${res.statusCode} - BODY: ${body}`
  );
}

export function loggerMiddleware(req, res, next) {
  /* TODO: Create unit test (but this is a external framework events, how to 
           test effectively ???)
    Suggest create fake request and send to this, open de log file and
    check if logger is present, but is a verbose test and this non guarantee 
    if work in multiple scenarios (http proxy and another third part libs events)
  */
  inputLogger(req);

  const send = res.send;
  res.send = function(body) {
    outputLogger(req, res, body);
    send.call(this, body);
  };

  next();
}
