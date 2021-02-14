import { MCQStore } from "./MedusaMCQ";
import { UserStore } from "./User";
import { action, observable } from "mobx";

// Root Store Declaration
export class RootStore {
  @observable mcqStore!: MCQStore;
  @observable userStore!: UserStore;

  constructor() {
    // this.authStore = new AuthStore(this);
    this.addMCQStore(new MCQStore(this))
    this.addUserStore(new UserStore(this))
  }

  @action
  addMCQStore = (store: MCQStore) => {
    this.mcqStore = store;

  }
  @action
  addUserStore = (store: UserStore) => {
    this.userStore = store;

  }
}
