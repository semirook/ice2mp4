# coding=utf-8
from werkzeug import secure_filename
from flask.templating import render_template
from flask.views import MethodView
from flask import redirect, request, url_for, current_app, send_from_directory

from . import base
from .forms import SubmitForm
from bl.helpers import ice_send_file, ice_convert_to_mp4



class FrontView(MethodView):

    def get(self):
        form = SubmitForm()
        return render_template(
            'base/main.html', reply_form=form,
        )

    def post(self):
        form = SubmitForm(request.form)
        input_file = request.files['video']
        if input_file:
            filename = secure_filename(input_file.filename)
            ice_send_file(filename, input_file)
            output_file_name = ice_convert_to_mp4(filename)
            return redirect(
                url_for('base.uploaded_file', filename=output_file_name)
            )

        return render_template(
            'base/main.html', reply_form=form,
        )

@base.route('uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(
        current_app.config['UPLOAD_PATH'],
        filename,
    )

base.add_url_rule('', view_func=FrontView.as_view('front_page'))
