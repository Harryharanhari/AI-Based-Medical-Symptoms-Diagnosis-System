from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models import Doctor, Appointment
from app.forms import AppointmentForm
from datetime import datetime

bp = Blueprint('appointments', __name__)

@bp.route('/appointments', methods=['GET', 'POST'])
@login_required
def book():
    form = AppointmentForm()
    doctors = Doctor.query.all()
    form.doctor.choices = [(d.id, f"Dr. {d.name} ({d.specialization})") for d in doctors]

    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=form.doctor.data,
            date=form.date.data,
            time_slot=form.time_slot.data,
            status='Pending'
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment request submitted successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    appointments = Appointment.query.filter_by(patient_id=current_user.id).all()
    return render_template('appointments/book.html', form=form, appointments=appointments)

@bp.route('/appointments/doctor')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Simple logic: doctors see all appointments for now
    appointments = Appointment.query.all()
    return render_template('appointments/doctor_dashboard.html', appointments=appointments)

@bp.route('/appointments/update_status/<int:appointment_id>/<string:status>')
@login_required
def update_status(appointment_id, status):
    appointment = Appointment.query.get_or_404(appointment_id)

    # doctors and admins can modify any appointment
    if current_user.role in ['doctor', 'admin']:
        appointment.status = status
    # patients may only cancel their own pending/confirmed appointments
    elif current_user.role == 'patient':
        if status != 'Cancelled' or appointment.patient_id != current_user.id:
            flash('Access denied.', 'danger')
            return redirect(url_for('main.dashboard'))
        appointment.status = status
    else:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.commit()
    flash(f'Appointment #{appointment_id} updated to {status}.', 'success')

    # redirect back to appropriate view
    if current_user.role == 'doctor':
        return redirect(url_for('appointments.doctor_dashboard'))
    elif current_user.role == 'patient':
        # return to booking/history page so patient sees updated list
        return redirect(url_for('appointments.book'))
    return redirect(url_for('main.dashboard'))
