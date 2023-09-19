from flask import flash, render_template, redirect, url_for

from . import app, db
from .forms import ShortURLForm
from .models import URLMap
from .api_views import get_unique_short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = ShortURLForm()
    if form.validate_on_submit():
        shortlink = form.custom_id.data or get_unique_short_link()
        url_commit = URLMap(
            original=form.original_link.data,
            short=shortlink
        )
        db.session.add(url_commit)
        db.session.commit()
        flash(url_for('index_view', short=shortlink, _external=True))
    return render_template('main.html', form=form)


@app.route('/<string:short>')
def short_view(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )