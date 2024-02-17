from flask import request, render_template, flash, url_for, redirect
from flask import current_app as app
from flask_login import login_required, current_user
from application.database import db
from application.models import Venue, Show


@app.route('/admin/add_show', methods=['GET', 'POST'])
@login_required
def add_show():
    if not current_user.is_admin():
        flash('You do not have permission to access the admin page.')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        rating = float(request.form['rating'])
        tags = request.form['tags']
        timing = request.form['timing']
        ticket_price = float(request.form['ticket_price'])
        venue_id = int(request.form['venue_id'])
        capacity = Venue.query.filter_by(id=venue_id).first().capacity

        show = Show(name=name,
                    rating=rating,
                    tags=tags,
                    timing=timing,
                    ticket_price=ticket_price,
                    capacity=capacity,
                    venue_id=venue_id)
        db.session.add(show)
        db.session.commit()
        flash('Show added successfully')
        return redirect(url_for('admin'))

    venues = Venue.query.all()
    return render_template('add_show.html', venues=venues)


@app.route('/admin/add_venue', methods=['GET', 'POST'])
@login_required
def add_venue():
    if not current_user.is_admin():
        flash('You do not have permission to access the admin page.')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        place = request.form['place']
        location = request.form['location']
        capacity = int(request.form['capacity'])

        venue = Venue(name=name,
                      place=place,
                      location=location,
                      capacity=capacity)
        db.session.add(venue)
        db.session.commit()
        flash('Venue added successfully.')
        return redirect(url_for('admin'))

    return render_template('add_venue.html')


@app.route('/admin/edit_venue/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_venue(id):
    if not current_user.is_admin():
        flash('You do not have permission to access the admin page.')
        return redirect(url_for('index'))

    venue = Venue.query.get(id)
    if not venue:
        flash('Invalid venue ID.')
        return redirect(url_for('admin'))

    if request.method == 'POST':
        name = request.form['name']
        place = request.form['place']
        location = request.form['location']
        capacity = int(request.form['capacity'])

        venue.name = name
        venue.place = place
        venue.location = location
        venue.capacity = capacity

        for show in venue.shows:
            show.capacity = capacity
        db.session.commit()

        flash('Venue updated successfully.')
        return redirect(url_for('admin'))

    return render_template('edit_venue.html', venue=venue)


@app.route('/admin/delete_venue/<int:id>')
@login_required
def delete_venue(id):
    if not current_user.is_admin():
        flash('You do not have permission to access the admin page.')
        return redirect(url_for('index'))

    venue = Venue.query.get(id)
    if not venue:
        flash('Invalid venue ID.')
        return redirect(url_for('admin'))

    for show in venue.shows:
        for ticket in show.tickets:
            db.session.delete(ticket)
        db.session.delete(show)

    db.session.delete(venue)
    db.session.commit()

    flash('Venue deleted successfully.')
    return redirect(url_for('admin'))


@app.route('/admin/edit_show/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_show(id):
    if not current_user.is_admin():
        flash('You do not have permission to access the admin page.')
        return redirect(url_for('index'))

    show = Show.query.get(id)
    if not show:
        flash('Invalid show ID.')
        return redirect(url_for('admin'))

    if request.method == 'POST':
        name = request.form['name']
        rating = float(request.form['rating'])
        tags = request.form['tags']
        timing = request.form['timing']
        ticket_price = float(request.form['ticket_price'])

        show.name = name
        show.rating = rating
        show.tags = tags
        show.timing = timing
        show.ticket_price = ticket_price
        db.session.commit()

        flash('Show updated successfully.')
        return redirect(url_for('admin'))

    return render_template('edit_show.html', show=show)


@app.route('/admin/delete_show/<int:id>')
@login_required
def delete_show(id):
    if not current_user.is_admin():
        flash('You do not have permission to access the admin page.')
        return redirect(url_for('index'))

    show = Show.query.get(id)
    if not show:
        flash('Invalid show ID.')
        return redirect(url_for('admin'))

    for ticket in show.tickets:
        db.session.delete(ticket)

    db.session.delete(show)
    db.session.commit()

    flash('Show deleted successfully.')
    return redirect(url_for('admin'))
