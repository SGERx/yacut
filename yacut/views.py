from flask import flash, render_template, redirect, url_for

from . import app, db
from .forms import ShortURLForm
from .models import URL_map
from .api_views import get_unique_short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = ShortURLForm()
    if form.validate_on_submit():
        shortlink = form.custom_id.data or get_unique_short_link()
        url_commit = URL_map(
            original=form.original_link.data,
            short=shortlink
        )
        db.session.add(url_commit)
        db.session.commit()
        flash(url_for('opinion_view', short=shortlink, _external=True))
    return render_template('main.html', form=form)


@app.route('/<string:short>')
def opinion_view(short):
    return redirect(
        URL_map.query.filter_by(short=short).first_or_404().original
    )
