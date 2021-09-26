from django import template
from django.utils.safestring import mark_safe

from medusa_website.mcq_bank.models import Answer, Question, QuizSession

register = template.Library()


@register.filter
def answer_choice_to_string(question, answer):
    return question.answer_choice_to_string(answer)


@register.simple_tag
def quiz_session_answer_for_question(quiz_session: QuizSession, question: Question) -> Answer:
    return quiz_session.user_answer_for_question(question)


@register.simple_tag
def clickable_image(image_url, alt_text, click_to_enlarge=True, max_width="30vw", max_height="50vh", padding="10px"):
    html = f"""
    <a href=""
       onclick="window.open('{image_url}','targetWindow', 'toolbar=no, location=no, status=no, menubar=no, scrollbars=yes, resizable=yes'); return false;">
      <img src="{image_url}" alt="{alt_text}"
           style="max-width: {max_width}; max-height: {max_height}; padding: {padding}"/>
    </a>
    """
    if click_to_enlarge:
        html += "<p><i>(click to enlarge)</i></p>"
    return mark_safe(html)
