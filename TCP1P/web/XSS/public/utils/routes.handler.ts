import { Application } from "../deps.ts";
import { Router } from "../deps.ts";

export class RoutesHandler {
  router: Router;
  app: Application;
  constructor(app: Application, callback: (router: Router) => void) {
    this.app = app;
    this.router = new Router();
    callback(this.router);
    this.app.use(this.router.routes());
    this.app.use(this.router.allowedMethods());
  }
}
