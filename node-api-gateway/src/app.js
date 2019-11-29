import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import helmet from 'helmet';
import cookieParser from 'cookie-parser';

import { AuthMiddleware } from './shared/middleware/auth';
import { TraceMiddleware } from './shared/middleware/trace';
import { loggerMiddleware } from './shared/middleware/logger';
import { AuthRoute, AccountRoute, RssRoute } from './shared/routers';

class App {
  constructor() {
    this.express = express();
    this.express.use(bodyParser.json({ limit: '20mb' }));
    this.express.use(cors());
    this.express.use(helmet());
    this.express.use(cookieParser());

    this.mountSecurity();
    this.mountRouters();
  }

  mountSecurity() {
    this.express.use(TraceMiddleware);
    this.express.use(AuthMiddleware);
    this.express.use(loggerMiddleware);
  }

  mountRouters() {
    const router = express.Router();

    router.get('/', (req, res) => {
      res.json({
        message: 'Api Gateway'
      });
    });

    this.express.use('/', router);
    this.express.all('/v1/auth*', AuthRoute);
    this.express.all('/v1/accounts*', AccountRoute);
    this.express.all('/v1/rss*', RssRoute);
  }
}

export default new App().express;
