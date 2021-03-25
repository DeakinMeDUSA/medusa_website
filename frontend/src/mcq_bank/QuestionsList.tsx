import React, { forwardRef } from "react";
import { action, observable } from "mobx";
import { RootStore } from "./RootStore";
import { Observer, observer } from "mobx-react";
import MaterialTable, { Icons } from "material-table";
import {
  AddBox,
  ArrowUpward,
  Block,
  Check,
  ChevronLeft,
  ChevronRight,
  Clear,
  DeleteOutline,
  Edit,
  FilterList,
  FirstPage,
  LastPage,
  List,
  Remove,
  SaveAlt,
  Search,
  ViewColumn,
} from "@material-ui/icons";
import axios from "axios";
import styled from "styled-components";
import { Button, Modal } from "react-bootstrap";

const tableIcons: Icons = {
  Add: forwardRef((props, ref) => <AddBox {...props} ref={ref}/>),
  Check: forwardRef((props, ref) => <Check {...props} ref={ref}/>),
  Clear: forwardRef((props, ref) => <Clear {...props} ref={ref}/>),
  Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref}/>),
  DetailPanel: forwardRef((props, ref) => <ChevronRight {...props} ref={ref}/>),
  Edit: forwardRef((props, ref) => <Edit {...props} ref={ref}/>),
  Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref}/>),
  Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref}/>),
  FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref}/>),
  LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref}/>),
  NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref}/>),
  PreviousPage: forwardRef((props, ref) => <ChevronLeft {...props} ref={ref}/>),
  ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref}/>),
  Search: forwardRef((props, ref) => <Search {...props} ref={ref}/>),
  SortArrow: forwardRef((props, ref) => <ArrowUpward {...props} ref={ref}/>),
  ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref}/>),
  ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref}/>),
};

interface questionData {
  id: number
  author: string
  question_text: string
  image: string
  category: string
}

interface answerData {
  id: number
  question_id: number
  answer_text: string
  is_correct: boolean
}

interface answerRecordData {
  // These are all ids, but aren't named with _id so they match the rest framework
  question: number
  answer: number
  user: number
}

const IsCorrectIcon = styled.img`
  height: 20px;
  width: 20px;
`

const ReviewQuestionsButton = styled.button`
  background: red;
  border: none;
  height: 40px;
  width: 600px;
  font-size: 14px;
  text-align: center;
`;

// TODO single source of truth for this, see models/question.py
const questionCategories = {
  UNCATEGORISED: "Uncategorised",
  CARDIOLOGY: "Cardiology",
  NEUROLOGY: "Neurology",
  PAEDIATRICS: "Paediatrics",
}

const questionColumns = [
  { title: "id", field: "id", hidden: false, grouping: false },
  { title: "Question Text", field: "question_text", grouping: false },
  { title: "Category", field: "category", grouping: true, lookup: questionCategories },
  { title: "Author", field: "author", grouping: true },
  { title: "Image url", field: "image", grouping: false },
]

const answerEditColumns = [
  { title: "id", field: "id", hidden: true, grouping: false },
  { title: "question_id", field: "question_id", hidden: true, grouping: false },
  { title: "Answer Text", field: "answer_text", grouping: false },
  {
    title: "Is Correct", field: "is_correct", lookup: { true: <Check/>, false: <Block/> },
    // @ts-ignore
    render: (rowData: answerData) => rowData.is_correct ? <Check/> : <Block/>
  },
]

const answerReviewColumns = [
  { title: "id", field: "id", hidden: true, grouping: false },
  { title: "question_id", field: "question_id", hidden: true, grouping: false },
  { title: "Answer Text", field: "answer_text", grouping: false },
]

class MCQAPI {
  rootURL = "http://localhost:8000/"

  async getQuestions({ per_page, page_n }: { per_page: number, page_n: number }): Promise<any> {
    return await axios.get(this.rootURL.concat("mcq_bank/api/questions"), {
      "data": {
        per_page: per_page,
        page_n: page_n
      }
    })
  }

  async getQuestion(question_id: number): Promise<any> {
    return await axios.get(this.rootURL.concat("mcq_bank/api/question/").concat(question_id.toString()))
  }

  async addQuestion(questionInfo: questionData): Promise<any> {
    return await axios.post(this.rootURL.concat("mcq_bank/api/questions"),
      questionInfo)
  }

  async deleteQuestion(questionInfo: questionData): Promise<any> {
    return await axios.delete(this.rootURL.concat("mcq_bank/api/question/").concat(questionInfo.id.toString()))
  }

  async modifyQuestion(questionInfo: questionData): Promise<any> {
    return await axios.put(this.rootURL.concat("mcq_bank/api/question/").concat(questionInfo.id.toString()),
      questionInfo)
  }

  async addAnswer(answerInfo: answerData): Promise<any> {
    return await axios.post(this.rootURL.concat("mcq_bank/api/answer/create"),
      answerInfo)
  }

  async deleteAnswer(answerInfo: answerData): Promise<any> {
    return await axios.delete(this.rootURL.concat("mcq_bank/api/answer/").concat(answerInfo.id.toString()))
  }

  async modifyAnswer(answerInfo: answerData): Promise<any> {
    return await axios.put(this.rootURL.concat("mcq_bank/api/answer/").concat(answerInfo.id.toString()),
      answerInfo)
  }

  async SubmitAnswerRecord(answerSubmit: answerRecordData): Promise<any> {
    return await axios.post(this.rootURL.concat("mcq_bank/api/record/create"), answerSubmit)
  }

  async getQAnswers(question_id: number): Promise<any> {
    console.log(`getQAnswers() : question_id = ${question_id}`)
    return await axios.get(this.rootURL.concat(`mcq_bank/api/answers?question_id=${question_id}`))
  }
}

export class MCQStore {
  @observable questions!: questionData[];
  @observable answers: any
  @observable rootStore!: RootStore;
  @observable api!: MCQAPI
  @observable curQuestionId!: number
  @observable curQuestion!: questionData
  @observable showQuestionEdit!: boolean
  @observable showQuestionReview!: boolean
  @observable questionsToReview!: questionData[]
  @observable questionReviewIdx!: number
  @observable selectedAnswerId!: number

  constructor(rootStore: RootStore) {
    this.addRootStore(rootStore)
    this.addMCQAPI(new MCQAPI())
    this.setDefaultVals()

  }

  @action
  setDefaultVals = () => {
    this.curQuestionId = -1
    this.curQuestion = { id: -1, author: "", question_text: "", image: "", category: "Uncategorised" }
    this.showQuestionEdit = false
    this.showQuestionReview = false
    this.questionReviewIdx = 0
    this.questionsToReview = []
    this.questions = []
    this.selectedAnswerId = -1
  }

  @action
  addRootStore = (store: RootStore) => {
    this.rootStore = store;
  }

  @action
  addMCQAPI = (api: MCQAPI) => {
    this.api = api;

  }

  @action
  setQuestions(questions: any) {
    this.questions = questions
  }

  @action
  setQuestionsToReview(questions: any) {
    this.questionsToReview = questions
  }

  @action
  setQuestion(question: questionData) {
    this.curQuestion = question
    this.curQuestionId = question.id
  }

  @action
  setSelectedAnswer(answerId: number) {
    this.selectedAnswerId = answerId
  }

  @action
  setAnswers(answers: any) {
    console.log(`Setting answers to ${JSON.stringify(answers)}`)
    this.answers = answers
  }

  @action
  setQuestionid(questionId: number) {
    this.curQuestionId = questionId
  }

  @action
  handleAnswerAdd = (answerInfo: answerData) => {
    return (this.api.addAnswer(this.updateAnsWithQID(answerInfo, this.curQuestionId))
      .then(() => {
        return this.api.getQAnswers(answerInfo.question_id)
      })
      .then((result) => {
        this.setAnswers(result.data)
      }))
  }
  @action
  handleAnswerModify = (answerInfo: answerData) => {
    return (
      this.api.modifyAnswer(this.updateAnsWithQID(answerInfo, this.curQuestionId))
        .then(() => {
          return this.api.getQAnswers(answerInfo.question_id)
        })
        .then((result) => {
          this.setAnswers(result.data)
        })
    )
  }
  @action
  handleAnswerDelete = (answerInfo: answerData) => {
    console.log(answerInfo)
    return (
      this.api.deleteAnswer(this.updateAnsWithQID(answerInfo, this.curQuestionId))
        .then(() => {
          return this.api.getQAnswers(answerInfo.question_id)
        })
        .then((result) => {
          this.setAnswers(result.data)
        })
    )
  }

  @action
  handleShowQuestionEdit = (question_id: number) => {

    this.api.getQuestion(question_id).then((result) => {
      this.setQuestion(result.data)
    })
    this.api.getQAnswers(question_id).then((result) => {
      this.setAnswers(result.data)
    })

    this.curQuestionId = question_id
    this.showQuestionEdit = true
  }

  @action
  handleShowQuestionReview = (question_id: number) => {

    this.api.getQuestion(question_id).then((result) => {
      this.setQuestion(result.data)
    })
    this.api.getQAnswers(question_id).then((result) => {
      this.setAnswers(result.data)
    })

    this.curQuestionId = question_id
    this.showQuestionReview = true
  }

  @action
  handleHideQuestionEdit = () => {
    this.showQuestionEdit = false
  }
  @action
  handleHideQuestionReview = () => {
    this.showQuestionReview = false
    this.questionReviewIdx = 0
    this.questionsToReview = []
    this.selectedAnswerId = -1

  }
  @action
  handleSkipQuestionReview = () => {
    this.questionReviewIdx = this.questionReviewIdx + 1
    this.selectedAnswerId = -1
    if (this.questionReviewIdx < this.questionsToReview?.length) {
      this.setQuestion(this.questionsToReview[this.questionReviewIdx])
      this.api.getQAnswers(this.curQuestionId).then((result) => {
        this.setAnswers(result.data)
      })
    } else {
      alert("No more questions remain, closing")
      this.handleHideQuestionReview()
    }
  }

  @action
  updateAnsWithQID(answerInfo: answerData, questionId: number) {
    answerInfo.question_id = questionId
    return answerInfo
  }

  @action
  startQuestionReview(include_answered = true, max_questions: number = 30) {
    this.api.getQuestions({ per_page: 0, page_n: 0 }).then((result) => {
      this.setQuestionsToReview(result.data);
      // @ts-ignore
      console.log(this.questionsToReview.toString())
      console.log("Loaded questions to review as above")
      if (this.questionsToReview.length > 1) {
        this.handleShowQuestionReview(this.questionsToReview[0].id)
      } else {
        alert("No questions found?")
      }
    })
  }

  @action
  handleQuestionReviewSubmit = () => {
    // this.rootStore.userStore.
    if (this.selectedAnswerId !== null) {
      console.log({
        answer_id: this.selectedAnswerId,
        question_id: this.curQuestionId
      })
      this.api.SubmitAnswerRecord({
        answer: this.selectedAnswerId,
        question: this.curQuestionId,
        user: 2, // test@medusa.org.au
      })
    }
  }
}

const QuestionImg = styled.img`
  height: 300px;
  //width: 200px;
`

const QuestionTextDiv = styled.div`
  font-size: 15px;
  padding: 5px;
`

const QuestionDetailDiv = styled.div`
  padding: 5px;
`

const QuestionEditPopup = observer(({ store }: { store: RootStore }) => {
  return (
    <Modal
      show={store.mcqStore.showQuestionEdit}
      onHide={store.mcqStore.handleHideQuestionEdit}
      centered={true}
      size="lg"
    >
      <Modal.Header closeButton>
        <Modal.Title>Edit Answers</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <QuestionDetailDiv>
          <QuestionTextDiv>
            <b>Question: </b>{store.mcqStore.curQuestion.question_text}
            <br/>
            <b>Category: </b>{store.mcqStore.curQuestion.category}
            <br/>
          </QuestionTextDiv>
          {store.mcqStore.curQuestion.image !== null ? <QuestionImg src={store.mcqStore.curQuestion.image}/> : null}
          <MaterialTable
            title="Answers"
            columns={answerEditColumns}
            data={store.mcqStore.answers}
            icons={tableIcons}
            options={{ emptyRowsWhenPaging: false, search: false, paging: false }}
            editable={{
              // @ts-ignore
              onRowAdd: (newData) => store.mcqStore.handleAnswerAdd(newData),
              // @ts-ignore
              onRowDelete: (oldData) => store.mcqStore.handleAnswerDelete(oldData),
              // @ts-ignore
              onRowUpdate: (newData) => store.mcqStore.handleAnswerModify(newData)
            }}
          />
        </QuestionDetailDiv>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={store.mcqStore.handleHideQuestionEdit}>
          Close
        </Button>
        <Button variant="primary" onClick={store.mcqStore.handleHideQuestionEdit}>
          Save Changes
        </Button>
      </Modal.Footer>
    </Modal>
  )
})


const QuestionReviewPopup = observer(({ store }: { store: RootStore }) => {
  return (
    <Modal
      show={store.mcqStore.showQuestionReview}
      onHide={store.mcqStore.handleHideQuestionReview}
      centered={true}
      size="lg"
    >
      <Modal.Header closeButton>
        <Modal.Title>Reviewing
          question {store.mcqStore.questionReviewIdx + 1} of {store.mcqStore.questionsToReview.length}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <QuestionDetailDiv>
          <QuestionTextDiv>
            <b>Question: </b>{store.mcqStore.curQuestion.question_text}
            <br/>
            <b>Category: </b>{store.mcqStore.curQuestion.category}
            <br/>
          </QuestionTextDiv>
          {store.mcqStore.curQuestion.image !== null ? <QuestionImg src={store.mcqStore.curQuestion.image}/> : null}
          <MaterialTable
            title="Select Answer(s)"
            columns={answerReviewColumns}
            data={store.mcqStore.answers}
            icons={tableIcons}
            options={{ emptyRowsWhenPaging: false, search: false, paging: false, selection: true }}
            editable={{}}
            onSelectionChange={(rows) => {
              if (rows.length === 1) {
                console.log(`Selected answer ${rows[0]}`)
                // @ts-ignore
                store.mcqStore.setSelectedAnswer(rows[0].id)
              }
            }}
          />
        </QuestionDetailDiv>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={store.mcqStore.handleHideQuestionReview}>
          Stop Question Review
        </Button>
        <Button variant="secondary" onClick={store.mcqStore.handleSkipQuestionReview}>
          Skip Question
        </Button>
        <Button variant="primary" onClick={store.mcqStore.handleQuestionReviewSubmit}>
          Submit Question
        </Button>
      </Modal.Footer>
    </Modal>
  )
})


export const QuestionsList = observer(({ store }: { store: RootStore }) => {
    return (
      <>
        <div>
          <span>This is the MedusaMCQ page</span>
          <ReviewQuestionsButton onClick={() => store.mcqStore.startQuestionReview()}>
            Review all questions
          </ReviewQuestionsButton>
          <Observer>{() =>
            <MaterialTable
              title={`All MCQ Questions`}
              columns={questionColumns}
              data={query => store.mcqStore.api.getQuestions({ per_page: query.pageSize, page_n: query.page })}
              icons={tableIcons}
              editable={{
                // @ts-ignore
                onRowAdd: (newData) => store.mcqStore.api.addQuestion(newData),
                // @ts-ignore
                onRowDelete: (oldData) => store.mcqStore.api.deleteQuestion(oldData),
                // @ts-ignore
                onRowUpdate: (newData) => store.mcqStore.api.modifyQuestion(newData)
              }}

              onRowClick={(event, rowData) => {
                // @ts-ignore
                store.mcqStore.handleShowQuestionEdit(rowData.id)
              }}
              options={{ grouping: true }}
              actions={[
                {
                  icon: List,
                  tooltip: 'Edit Answers',
                  onClick: (event, rowData) => {
                    // @ts-ignore
                    store.mcqStore.handleShowQuestionEdit(rowData.id)
                  }
                }
              ]}
            />
          }</Observer>

        </div>
        <QuestionEditPopup store={store}/>
        <QuestionReviewPopup store={store}/>
      </>
    )
  }
)
