from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional, Regexp, ValidationError
from .models import URL_map


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
        'Введите вариант короткой ссылки',
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

    def validate_custom_id(self, field):
        if field.data and URL_map.query.filter_by(short=field.data).first():
            raise ValidationError(f'Имя {field.data} уже занято!')