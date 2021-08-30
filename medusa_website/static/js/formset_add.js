// Allows the addition of formset rows, like what is in django admin
function addForm(e) {
  e.preventDefault()
  let answerForms = $('tr.answer-form-row')
  let container = document.querySelector('tbody.answer-form-body')
  let totalForms = document.querySelector('#id_answers-TOTAL_FORMS')
  let formNum = answerForms.length - 1// Get the number of the last form on the page with zero-based indexing

  let newForm = answerForms[0].cloneNode(true) //Clone the bird form
  let formRegex = RegExp(`answers-(\\d){1}-`, 'g') //Regex to find all instances of the form number

  formNum++ //Increment the form number
  newForm.innerHTML = newForm.innerHTML.replace(formRegex, `answers-${formNum}-`) //Update the new form to have the correct form number
  // remove existing values
  text_values = newForm.querySelectorAll('input[type=text]')
  text_values.forEach(element => element.setAttribute('value', ''))

  let newRow = container.insertRow() //Insert a new row
  newRow.innerHTML = newForm.innerHTML
  totalForms.setAttribute('value', `${formNum + 1}`) //Increment the number of total forms in the management form
}

$(document).ready(function () {
  let addButton = document.querySelector('#add-answer')
  addButton.addEventListener('click', addForm)
})
