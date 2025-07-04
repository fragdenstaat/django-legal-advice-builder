import io

from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Answer, Question
from .signals import answer_created
from .utils import get_answer_from_list


class GenrateFormWizardMixin:
    def get_initial_dict(self):
        return {}

    def _get_dict_entry_for_question(self, question):
        initial_dict = self.get_initial_dict()
        questionaire = question.questionaire
        if questionaire.short_title and question.short_title:
            questionaire_dict = initial_dict.get(questionaire.short_title)
            if questionaire_dict:
                return questionaire_dict.get(question.short_title)

    def get_initial_data(self, question):
        question_data = self._get_dict_entry_for_question(question)
        if question_data and "initial" in question_data:
            text_types = [question.TEXT, question.SINGLE_LINE]
            single_option_types = [question.SINGLE_OPTION, question.YES_NO]
            if question.field_type in text_types:
                return {"text": question_data.get("initial")}
            elif question.field_type in single_option_types:
                return {"option": question_data.get("initial")}
            elif question.field_type == question.MULTIPLE_OPTIONS:
                return {"option": question_data.get("initial")}
            elif question.field_type == question.DATE:
                return {"date": question_data.get("initial")}

    def get_initial_options(self, question):
        question_data = self._get_dict_entry_for_question(question)
        if question_data and "options" in question_data:
            return question_data.get("options")
        return question.options

    def render_next(self, question, answers, initial_data=None):
        self.storage.set_data(
            {
                "current_questionaire": question.questionaire.id,
                "current_question": question.id,
                "answers": answers,
            }
        )
        initial_options = self.get_initial_options(question)
        if not initial_data:
            initial_data = self.get_initial_data(question)
        form = self.get_form(
            question=question, initial_data=initial_data, options=initial_options
        )
        return self.render_form(form)

    def get_current_question(self):
        question_id = self.storage.get_data().get("current_question")
        return Question.objects.get(id=question_id)

    def get_answer_for_question(
        self, question_short_title, questionaire_short_title=None
    ):
        filters = {"short_title": question_short_title}
        if questionaire_short_title:
            filters["questionaire__short_title"] = questionaire_short_title
        questions = Question.objects.filter(**filters)
        if questions:
            answers = self.storage.get_data().get("answers")
            question = questions.first()
            answers = self.storage.get_data().get("answers")
            if answers:
                return get_answer_from_list(answers, question)
        return ""

    def get_form(self, question=None, data=None, initial_data=None, options=None):
        form_class = self.wizard_form_class
        form_kwargs = {
            "question": question,
            "data": data,
            "initial": initial_data,
            "options": options,
        }
        return form_class(**form_kwargs)

    def render_form(self, form=None, **kwargs):
        form = form or self.get_form()
        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)

    def validate_form_and_get_next(self, question=None, answers=None, data=None):
        initial_options = self.get_initial_options(question)
        question_form = self.get_form(
            question=question, data=self.request.POST, options=initial_options
        )
        if question_form.is_valid():
            cleaned_data = question_form.cleaned_data
            status = question.get_status(
                option=cleaned_data.get("option"),
                text=cleaned_data.get("text"),
                date=cleaned_data.get("date"),
            )
            next_question = status.get("next")
            answers = answers + [cleaned_data]
            if not status.get("ongoing"):
                self.storage.set_data(
                    {
                        "current_questionaire": question.questionaire.id,
                        "current_question": question.id,
                        "answers": answers,
                    }
                )
                return self.render_status(**status)
            elif next_question:
                return self.render_next(next_question, answers)
            else:
                return self.render_done(answers)
        else:
            return self.render_form(question_form)

    def render_status(self, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def render_done(self, answers=None, **kwargs):
        context = self.get_template_with_context(answers)
        if self.law_case.save_answers:
            answer = self.save_answers(answers)
            form = self.get_answer_template_form(answer)
            preview = answer.rendered_document
            context.update({"answer_form": form, "preview": preview})
        return self.render_to_response(context)


class GenerateEditableDocumentMixin:
    def save_answers(self, answers):
        answer = Answer.objects.create(
            law_case=self.get_lawcase(),
            answers=answers,
        )
        answer_created.send(sender=answer)
        if self.request.user.is_authenticated:
            answer.creator = self.request.user
            answer.save()
        return answer

    def save_document_form(self, data, answer, **kwargs):
        answer_form = self.document_form_class(data=data, instance=answer)
        if answer_form.is_valid():
            answer_form.save()

    def render_document_form(self, data, answer, **kwargs):
        answer_form = self.document_form_class(data=data, instance=answer)
        if answer_form.is_valid():
            answer_form.save()
        preview = answer.rendered_document
        context = self.get_context_data(**kwargs)
        context.update(
            {"answer": answer, "answer_form": answer_form, "preview": preview}
        )
        return self.render_to_response(context)

    def get_answer_template_form(self, answer):
        answer.save_rendered_document()
        document_form_class = self.document_form_class
        return document_form_class(instance=answer)


class GeneratePDFDownloadMixin:
    def get_html_string(self, answers):
        context = self.get_template_with_context(answers)
        return render_to_string(self.download_template_name, context)

    def get_template_with_context(self, answers, **kwargs):
        template = self.get_lawcase().document.template_with_answers(answers)
        return self.get_context_data(template=template, **kwargs)

    def get_filename(self):
        return "download"

    def get_pdf_bytes(self, html_string):
        import weasyprint as wp

        doc = wp.HTML(string=html_string)
        return doc.write_pdf(
            stylesheets=[
                wp.CSS(string="body { font-family: sans-serif !important }"),
                wp.CSS(string="@page { size: A4; margin: 2cm }"),
                wp.CSS(string="body { font-size: 14px !important }"),
                wp.CSS(string="body { line-height: 1.5 !important }"),
            ]
        )

    def render_pdf_download_response(self, answers, answer=None):
        html_string = ""
        if answer:
            html_string = answer.rendered_document
        else:
            html_string = self.get_html_string(answers)
        return self.generate_pdf_download(html_string)

    def generate_pdf_download(self, html_string):
        response = HttpResponse(
            self.get_pdf_bytes(html_string), content_type="application/pdf"
        )
        filename = self.get_filename()
        attachment = 'attachment; filename="{}{}"'.format(filename, ".pdf")
        response["Content-Disposition"] = attachment
        return response


class GenerateWordDownloadMixin:
    def get_word_from_html(self, html_string):
        from docx import Document
        from htmldocx import HtmlToDocx

        document = Document()
        new_parser = HtmlToDocx()
        new_parser.add_html_to_document(html_string, document)
        doc_io = io.BytesIO()
        document.save(doc_io)
        doc_io.seek(0)
        return doc_io

    def get_template_with_context(self, answers, **kwargs):
        template = self.get_lawcase().document.template_with_answers(answers)
        return self.get_context_data(template=template, **kwargs)

    def get_html_string(self, answers):
        context = self.get_template_with_context(answers)
        return render_to_string(self.download_template_name, context)

    def render_word_download_response(self, answers, answer=None):
        html_string = ""
        if answer:
            html_string = answer.rendered_document
        else:
            html_string = self.get_html_string(answers)
        return self.generate_word_download(html_string)

    def get_filename(self):
        return "download"

    def generate_word_download(self, html_string):
        response = HttpResponse(
            self.get_word_from_html(html_string).read(),
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        filename = self.get_filename()
        attachment = 'attachment; filename="{}{}"'.format(filename, ".docx")
        response["Content-Disposition"] = attachment
        return response


class GenerateHTMLDownloadMixin:
    def get_html(self, html_string):
        return html_string

    def get_template_with_context(self, answers, **kwargs):
        template = self.get_lawcase().document.template_with_answers(answers)
        return self.get_context_data(template=template, **kwargs)

    def get_html_string(self, answers):
        context = self.get_template_with_context(answers)
        return render_to_string(self.download_template_name, context)

    def render_html_download_response(self, answers, answer=None):
        html_string = ""
        if answer:
            html_string = answer.rendered_document
        else:
            html_string = self.get_html_string(answers)
        return self.generate_html_download(html_string)

    def get_filename(self):
        return "download"

    def generate_html_download(self, html_string):
        response = HttpResponse(self.get_html(html_string))
        filename = self.get_filename()
        attachment = 'attachment; filename="{}{}"'.format(filename, ".html")
        response["Content-Disposition"] = attachment
        return response
