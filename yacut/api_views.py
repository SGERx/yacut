from http import HTTPStatus
from random import choices
from re import match
from string import ascii_letters, digits

from flask import jsonify, request

from yacut import app, db

from .error_handlers import InvalidAPIUsageError
from .models import URLMap


def get_unique_short_link():
    while True:
        short_id = ''.join(choices(ascii_letters + digits, k=6))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsageError('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsageError('"url" является обязательным полем!')
    if not match(
            r'^[a-z]+://[^\/\?:]+(:[0-9]+)?(\/.*?)?(\?.*)?$', data['url']):
        raise InvalidAPIUsageError('Указан недопустимый URL')
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_link()
    if not match(r'^[A-Za-z0-9]{1,16}$', data['custom_id']):
        raise InvalidAPIUsageError(
            'Указано недопустимое имя для короткой ссылки')
    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsageError(f'Имя "{data["custom_id"]}" уже занято.')
    url_commit = URLMap()
    url_commit.from_dict(data)
    db.session.add(url_commit)
    db.session.commit()
    base = request.host_url
    return jsonify(short_link=base + url_commit.short, url=url_commit.original), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/')
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsageError(
            'Указанный id не найден', HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url.original})
