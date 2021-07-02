from django.db import models

from .question import Question


class Condition(models.Model):
    question = models.ForeignKey('legal_advice_builder.Question',
                                 on_delete=models.CASCADE)
    if_option = models.CharField(max_length=500)
    if_value = models.CharField(max_length=500)
    then_value = models.CharField(max_length=500)

    class Meta:
        unique_together = ['question', 'if_value', 'then_value']

    def __str__(self):
        return 'if answer {} "{}" then {}'.format(self.if_option,
                                                  self.if_value,
                                                  self.then_value)

    def update_questions(self):
        if self.question.options and 'question_' in self.then_value:
            question_id = self.then_value.split('_')[1]
            question = Question.objects.filter(id=question_id).first()
            if question:
                question.move(self.question, pos='last-child')
                question.refresh_from_db()
                question.parent_option = self.if_value
                question.save()
