import React, { forwardRef } from "react";
import { action, observable } from "mobx";
import { RootStore } from "../components/RootStore";
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

const IsCorrectIcon = styled.img`
  height: 20px;
  width: 20px;
`

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

const answerColumns = [
  { title: "id", field: "id", hidden: true, grouping: false },
  { title: "question_id", field: "question_id", hidden: true, grouping: false },
  { title: "Answer Text", field: "answer_text", grouping: false },
  {
    title: "Is Correct", field: "is_correct", lookup: { true: <Check/>, false: <Block/> },
    // @ts-ignore
    render: (rowData: answerData) => rowData.is_correct ? <Check/> : <Block/>
  },
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

  async getQAnswers(question_id: number): Promise<any> {
    console.log(`getQAnswers() : question_id = ${question_id}`)
    return await axios.get(this.rootURL.concat(`mcq_bank/api/answers?question_id=${question_id}`))
  }
}

export class MCQStore {
  @observable questions: questionData[] | undefined;
  @observable answers: any
  @observable rootStore!: RootStore;
  @observable api!: MCQAPI
  @observable curQuestionId!: number
  @observable curQuestion!: questionData
  @observable showQuestionEdit!: boolean

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
  setQuestion(question: questionData) {
    this.curQuestion = question
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
  handleHideQuestionEdit = () => {
    this.showQuestionEdit = false
  }

  @action
  updateAnsWithQID(answerInfo: answerData, questionId: number) {
    answerInfo.question_id = questionId
    return answerInfo
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
            columns={answerColumns}
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


export const MedusaMCQ = observer(({ store }: { store: RootStore }) => {
    return (
      <>
        <div>
          <span>This is the MedusaMCQ page</span>
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
      </>
    )
  }
)