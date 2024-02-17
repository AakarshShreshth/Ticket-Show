from flask import request, render_template, flash, url_for, redirect
from flask import current_app as app
from flask_login import login_required, current_user
from application.database import db
from application.models import Venue, Show, Ticket


@app.route('/', methods=['GET', 'POST'])
def index():
    location = ''
    if request.method == 'POST':
        location = request.form['location']
        venues = Venue.query.filter(
            Venue.location.ilike(f'%{location}%')).all()
    else:
        venues = Venue.query.all()
    dashboard = {venue: [] for venue in venues}
    for venue in venues:
        shows = Show.query.filter_by(venue_id=venue.id).order_by(
            Show.timing.asc()).all()
        dashboard[venue] = shows
    if (current_user.is_authenticated and current_user.is_admin()):
        return redirect(url_for('admin'))

    return render_template('index.html',
                           dashboard=dashboard,
                           location=location)


@app.route('/shows', methods=['GET', 'POST'])
def all_shows():
    if request.method == 'POST':
        search_query = request.form['search_query']
        shows = Show.query.filter(Show.name.ilike(f'%{search_query}%'))
        return render_template('shows.html',
                               shows=shows,
                               search_query=search_query)
    else:
        shows = Show.query.all()
        return render_template('shows.html', shows=shows)


@app.route('/shows/<int:id>')
def show_details(id):
    show = Show.query.get(id)
    if not current_user.is_authenticated:
        flash('You need to login to book tickets')
    return render_template('show_details.html', show=show)


@app.route('/book_tickets/<int:id>', methods=['GET', 'POST'])
@login_required
def book_tickets(id):
    if request.method == 'POST':
        quantity = int(request.form['quantity'])

        show = Show.query.get(id)
        if show:
            if quantity <= show.available_tickets():
                ticket = Ticket(quantity=quantity,
                                user_id=current_user.id,
                                show_id=id)
                db.session.add(ticket)
                db.session.commit()
                flash('Tickets booked successfully.', category="success")
                return redirect(url_for('profile'))
            else:
                flash('Not enough tickets available.')
        else:
            flash('Invalid show ID.')

    show = Show.query.filter_by(id=id).first()
    return render_template('book_tickets.html', show=show)


@app.route('/profile')
@login_required
def profile():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', tickets=tickets)
