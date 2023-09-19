from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional, Regexp


class ShortURLForm(FlaskForm):
    original_link = URLField(
        "Введите исходный URL",
        validators=(
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(require_tld=True, message='Ссылка некорректна')
        )
    )
    custom_id = StringField(
        validators=(
            Length(1, 16),
            Regexp(
                regex=r"[A-za-z0-9]+",
                message='Недопустимые символы в ссылке'
            ),
            Optional()
        )
    )
    submit = SubmitField('Создать')