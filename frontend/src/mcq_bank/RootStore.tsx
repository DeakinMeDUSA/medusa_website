import { MCQStore } from "./QuestionsList";
import { UserStore } from "./User";
import { action, observable } from "mobx";

// Root Store Declaration
export class RootStore {
  @observable mcqStore!: MCQStore;
  @observable userStore!: UserStore;
  @observable mode: string;

  constructor() {
    // this.authStore = new AuthStore(this);
    this.addMCQStore(new MCQStore(this))
    this.addUserStore(new UserStore(this))
    this.mode = "questions_list"

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
