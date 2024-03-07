from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = 'supersecretkey'


class UploadFileForm(FlaskForm):
    file = FileField("file")
    submit = SubmitField("Upload File")


@app.route('/', methods=['POST'])
@app.route('/homepage', methods=['POST'])
def homepage():
    form = UploadFileForm()
    return render_template('homepage.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
