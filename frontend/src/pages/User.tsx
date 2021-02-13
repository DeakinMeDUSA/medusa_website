import { observer } from "mobx-react";
import { RootStore } from "../components/RootStore";
import React from "react";
import { action, makeObservable, observable } from "mobx";
import axios from "axios";


export interface LoginValues {
  email: string;
  password: string;
}


class UserAPI {
  rootURL = "http://localhost:8000/"
  csrfToken: string | null = null

  async loginUser(data: LoginValues): Promise<any> {
    return await axios.post(this.rootURL.concat("token-auth/"),
      data,
      {
        headers: {
          'Content-Type': 'application/json',
          // 'X-CSRFToken': await this.getCsrfToken()
        }
      }
    )
  }

  async signupUser({ data }: { data: any }): Promise<any> {
    return await axios.post(this.rootURL.concat("users/users/"),
      data,
      {
        headers: {
          'Content-Type': 'application/json',
          // 'X-CSRFToken': await this.getCsrfToken()
        }
      })
  }

  async getUser(username: string | null): Promise<any> {
    if (username !== null) {
      return await axios.get(`${this.rootURL}users/current-user/`, {
        headers: {
          Authorization: `JWT ${localStorage.getItem('token')}`,
          // 'X-CSRFToken': await this.getCsrfToken()
        }
      })
    }
  }

  async getCsrfToken() {
    if (this.csrfToken === null) {
      const response = await fetch(this.rootURL.concat("csrf/"), {
        credentials: 'include',
      });
      const data = await response.json();
      this.csrfToken = data.csrfToken;
      console.log(`csrfToken = ${this.csrfToken}`)
    }
    return this.csrfToken;
  }


  // async getQuestions({ per_page, page_n }: { per_page: number, page_n: number }): Promise<any> {
  //   return await axios.get(this.rootURL.concat("mcq_bank/api/questions"), {
  //     "data": {
  //       per_page: per_page,
  //       page_n: page_n
  //     }
  //   })
  // }
  //
  // async getQuestion(question_id: number): Promise<any> {
  //   return await axios.get(this.rootURL.concat("mcq_bank/api/question/").concat(question_id.toString()))
  // }
  //
  // async addQuestion(questionInfo: questionData): Promise<any> {
  //   return await axios.post(this.rootURL.concat("mcq_bank/api/questions"),
  //     questionInfo)
  // }
  //
  // async deleteQuestion(questionInfo: questionData): Promise<any> {
  //   return await axios.delete(this.rootURL.concat("mcq_bank/api/question/").concat(questionInfo.id.toString()))
  // }
  //
  // async modifyQuestion(questionInfo: questionData): Promise<any> {
  //   return await axios.put(this.rootURL.concat("mcq_bank/api/question/").concat(questionInfo.id.toString()),
  //     questionInfo)
  // }
  //
  // async addAnswer(answerInfo: answerData): Promise<any> {
  //   return await axios.post(this.rootURL.concat("mcq_bank/api/answer/create"),
  //     answerInfo)
  // }
  //
  // async deleteAnswer(answerInfo: answerData): Promise<any> {
  //   return await axios.delete(this.rootURL.concat("mcq_bank/api/answer/").concat(answerInfo.id.toString()))
  // }
  //
  // async modifyAnswer(answerInfo: answerData): Promise<any> {
  //   return await axios.put(this.rootURL.concat("mcq_bank/api/answer/").concat(answerInfo.id.toString()),
  //     answerInfo)
  // }
  //
  // async getQAnswers(question_id: number): Promise<any> {
  //   console.log(`getQAnswers() : question_id = ${question_id}`)
  //   return await axios.get(this.rootURL.concat(`mcq_bank/api/answers?question_id=${question_id}`))
  // }
}

export class UserStore {
  rootStore: RootStore;
  api: UserAPI
  isLoggedIn: boolean
  username: string | null
  email: string
  displayedForm: string

  constructor(rootStore: RootStore) {
    makeObservable(this, {
      isLoggedIn: observable,
      username: observable,
      email: observable,
      displayedForm: observable,


      handleLogin: action,
      handleUserState: action,
      setUser: action,
      handleSignup: action,
      handleLogout: action,


    })
    this.rootStore = rootStore
    this.api = new UserAPI()
    this.isLoggedIn = localStorage.getItem('token') ? true : false
    this.username = this.isLoggedIn ? localStorage.getItem('username') : ""
    this.displayedForm = ""
    this.email = ""

    this.handleUserState()
  }


  // setQuestions(questions: any) {
  //   this.questions = questions
  // }
  //
  // setQuestion(question: questionData) {
  //   this.curQuestion = question
  // }
  //
  // setAnswers(answers: any) {
  //   console.log(`Setting answers to ${JSON.stringify(answers)}`)
  //   this.answers = answers
  // }
  //
  // setQuestionid(questionId: number) {
  //   this.curQuestionId = questionId
  // }
  //
  handleLogin = (data: any) => {
    return (this.api.loginUser(data)
      .then((result) => {
        this.setUser({ token: result.data.token, username: result.data.user.username })
      }))
  }

  handleUserState = () => {
    if (this.isLoggedIn) {
      this.api.getUser(localStorage.getItem('username'))
        .then(res => {
          console.log(res.data);
          this.setUser({
            username: res.data.username
          });
        });
    }
  }


  setUser = ({ token, username }: { token?: string, username: string }) => {
    if (token) {
      localStorage.setItem('token', token);
      localStorage.setItem('username', username);
    }
    this.isLoggedIn = true
    this.displayedForm = ""
    this.username = username

  }

  handleSignup = (data: any) => {
    return (this.api.signupUser(data)
      .then(result => this.setUser({ token: data.token, username: result.data.username })))
  }

  handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    this.isLoggedIn = false
    this.username = ""
  }

  // handleAnswerModify = (answerInfo: answerData) => {
  //   return (
  //     this.api.modifyAnswer(this.updateAnsWithQID(answerInfo, this.curQuestionId))
  //       .then(() => {
  //         return this.api.getQAnswers(answerInfo.question_id)
  //       })
  //       .then((result) => {
  //         this.setAnswers(result.data)
  //       })
  //   )
  // }
  // handleAnswerDelete = (answerInfo: answerData) => {
  //   console.log(answerInfo)
  //   return (
  //     this.api.deleteAnswer(this.updateAnsWithQID(answerInfo, this.curQuestionId))
  //       .then(() => {
  //         return this.api.getQAnswers(answerInfo.question_id)
  //       })
  //       .then((result) => {
  //         this.setAnswers(result.data)
  //       })
  //   )
  // }
  //
  // handleShowQuestionEdit = (question_id: number) => {
  //
  //   this.api.getQuestion(question_id).then((result) => {
  //     this.setQuestion(result.data)
  //   })
  //   this.api.getQAnswers(question_id).then((result) => {
  //     this.setAnswers(result.data)
  //   })
  //
  //   this.curQuestionId = question_id
  //   this.showQuestionEdit = true
  // }
  //
  // handleHideQuestionEdit = () => {
  //   this.showQuestionEdit = false
  // }
  //
  // updateAnsWithQID(answerInfo: answerData, questionId: number) {
  //   answerInfo.question_id = questionId
  //   return answerInfo
  // }
}


export const UserPage = observer(({ store }: { store: RootStore }) => {

  return (
    <div>This is the User page
      <h3>
        {store.userStore.isLoggedIn
          ? `Hello, ${store.userStore.username}`
          : "Not signed in"}
      </h3>

    </div>
  );
})
