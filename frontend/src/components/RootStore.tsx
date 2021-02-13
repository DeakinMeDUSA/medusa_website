import { MCQStore } from "../pages/MedusaMCQ";
import { AboutStore } from "../pages/About";
import { UserStore } from "../pages/User";
import { action, makeObservable, observable } from "mobx";

// Root Store Declaration
export class RootStore {
  mcqStore!: MCQStore;
  aboutStore!: AboutStore;
  userStore!: UserStore;

  constructor() {
    makeObservable(this, {
      mcqStore: observable,
      aboutStore: observable,
      userStore: observable,
      addMCQStore: action,
      addAboutStore: action,
      addUserStore: action,
    })
    // this.authStore = new AuthStore(this);
    this.addMCQStore(new MCQStore(this))
    this.addAboutStore(new AboutStore(this))
    this.addUserStore(new UserStore(this))
  }

  addMCQStore = (store: MCQStore) => {
    this.mcqStore = store;

  }
  addAboutStore = (store: AboutStore) => {
    this.aboutStore = store;

  }
  addUserStore = (store: UserStore) => {
    this.userStore = store;

  }
}
