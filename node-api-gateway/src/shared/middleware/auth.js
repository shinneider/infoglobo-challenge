import jwtDecode from 'jwt-decode';
import { inputLogger, outputLogger } from './logger';

function decodeToken(authorization) {
  try {
    return jwtDecode(authorization.substring(7));
  } catch (err) {
    return {};
  }
}

function AuthMiddleware(req, res, next) {
  req.headers['auth'] = false;
  req.headers['userId'] = null;

  if (req.headers['authorization']) {
    /* TODO: Check if token as expired and check if is a app token

      this middleware decode a jwt and get user information, but
      this no guarantee if this token is emited by a valid micro service

      Suggest auth micro service add all token in a cache system (like redis), 
      and find this token in a cache, is more secure, and has a control off all 
      token (easy to invalid a token and sig-out a user), another way is verify 
      token in auth micro service (but this generate high trafic for a micro 
      service, and is slow method)
    */
    const decoded = decodeToken(req.headers['authorization']);
    if (Object.keys(decoded).length >= 1) {
      delete req.headers['authorization'];
      req.headers['auth'] = true;
      req.headers['userId'] = decoded.user_id;
    } else {
      inputLogger(req);

      const output = { message: 'Provided token is invalid.' };
      res.status(401).json(output);

      outputLogger(req, res, JSON.stringify(output));
      return;
    }
  }

  next();
}

export { AuthMiddleware };
