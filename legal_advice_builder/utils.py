import datetime

import nh3


def generate_answers_dict_for_template(answers):
    from .models import Question

    answers_dict = {}
    for answer in answers:
        question = Question.objects.get(id=answer.get("question"))
        option = answer.get("option")
        text = answer.get("text")
        date = answer.get("date")
        if date:
            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                pass
        key, value = question.get_dict_key(option, text, date)
        answers_dict[key] = value
    return answers_dict


def only_text_align_css_properties(tag, attr, value):
    """Poor CSS parser to check if the value is a text-align property."""
    if attr == "style":
        props = value.split(";")
        for prop in props:
            if not prop.strip().startswith("text-align:"):
                return None

    return value


def clean_html_field(text, setting="default"):
    allowed_tags = {
        "p",
        "strong",
        "em",
        "u",
        "ol",
        "li",
        "ul",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
    }
    allowed_attrs = {"*": ["style"]}
    return nh3.clean(
        text,
        tags=allowed_tags,
        attributes=allowed_attrs,
        attribute_filter=only_text_align_css_properties,
    )


def get_answer_from_list(answers, question):
    for answer in answers:
        if answer.get("question") == str(question.id):
            option = answer.get("option")
            text = answer.get("text")
            date = answer.get("date")
            if date:
                try:
                    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                except ValueError:
                    pass
            return text or date or option
    return False
