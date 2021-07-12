import factory

from legal_advice_builder.models import Question


def get_single_option_question(questionaire=None):
    res_dict = {
        'text': factory.Faker('text'),
        'field_type': Question.SINGLE_OPTION,
        'options': {
            'yes': 'yes',
            'no': 'no',
            'maybe': 'maybe'
        }
    }
    if questionaire:
        res_dict.update({
            'questionaire': questionaire
        })
    return res_dict


def get_text_question(questionaire=None):
    res_dict = {
        'text': factory.Faker('text'),
        'field_type': Question.TEXT,
    }
    if questionaire:
        res_dict.update({
            'questionaire': questionaire
        })
    return res_dict


def get_date_question(questionaire=None):
    res_dict = {
        'text': factory.Faker('text'),
        'field_type': Question.DATE,
    }

    if questionaire:
        res_dict.update({
            'questionaire': questionaire
        })
    return res_dict
