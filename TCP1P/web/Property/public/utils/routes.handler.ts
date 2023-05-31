import { Application, Router } from "../deps.ts";
import { AppState } from "../deps.ts";

export class RoutesHandler {
  router: Router<AppState>;
  app: Application;
  constructor(
    app: Application,
    callback: (router: Router<AppState>) => void,
  ) {
    this.app = app;
    this.router = new Router<AppState>();
    callback(this.router);
    this.app.use(this.router.routes());
    this.app.use(this.router.allowedMethods());
  }
}
