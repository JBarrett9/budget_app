from flask import Blueprint, render_template, flash, url_for, redirect, abort, request
from flask_login import login_required, current_user

from budgetapp import db, bills
from budgetapp.bills.forms import AddBillForm
from budgetapp.models import Bill, PastBills

bills = Blueprint('bills', __name__)


@bills.route("/bills")
@login_required
def bill_index():
    bills = Bill.query.filter_by(user=current_user).order_by(Bill.due)
    return render_template('bill_templates/index.html', title='Bills', bills=bills)


@bills.route("/add_bill/<string:category>", methods=['GET', 'POST'])
@login_required
def add_bill(category):
    form = AddBillForm()
    if category == "subscription" or category == "rentMortgage":
        recurring = True
        fixed_amt = True
    elif category == "utility" or category == "pmtPlan":
        recurring =True
        fixed_amt = form.fixed_amt.data
    else:
        recurring = form.recurring.data
        fixed_amt = form.fixed_amt.data
    if form.validate_on_submit():
        bill = Bill(name=form.name.data, amount=form.amount.data, fixed_amt=fixed_amt, due=form.due.data,
                    recurring=recurring, frequency=form.frequency.data, category=category,
                    user=current_user)
        db.session.add(bill)
        db.session.commit()
        flash('Bill Added successfully', 'success')
        return redirect(url_for('bills.bill_index'))
    return render_template('bill_templates/add_bill.html', title='Add Bill', form=form, category=category)


@bills.route("/bill/<int:bill_id>")
@login_required
def bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    return render_template('bill_templates/bill.html', title=bill.id, bill=bill)


@bills.route("/bill/<int:bill_id>/delete", methods=['POST'])
@login_required
def delete_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    if bill.user_id != current_user.content_id:
        abort(403)
    db.session.delete(bill)
    db.session.commit()
    flash('Bill has been removed successfully', 'success')
    return redirect(url_for('bills.bill_index'))


@bills.route("/bill/<int:bill_id>/update", methods=['GET', 'POST'])
@login_required
def update_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    if bill.user_id != current_user.content_id:
        abort(403)
    form = AddBillForm()
    if form.validate_on_submit():
        bill.name = form.name.data
        bill.amount = form.amount.data
        bill.fixed_amt = form.fixed_amt.data
        bill.due = form.due.data
        bill.recurring = form.recurring.data
        bill.frequency = form.frequency.data
        db.session.commit()
        return redirect(url_for('bills.bill_index'))
    elif request.method == 'GET':
        form.name.data = bill.name
        form.amount.data = bill.amount
        form.fixed_amt.data = bill.fixed_amt
        form.due.data = bill.due
        form.recurring.data = bill.recurring
        form.frequency.data = bill.frequency
    return render_template('bill_templates/add_bill.html', title='Update Bill', form=form, legend='Update Bill')


@bills.route("/bill/<int:bill_id>/paid", methods=['GET', 'POST'])
@login_required
def paid(bill_id):
    frequency = {"once": 0, "weekly": 7, "bi-weekly": 14, "monthly": 1, "bi-monthly": 2, "yearly": 12}
    bill = Bill.query.get_or_404(bill_id)
    if bill.user_id != current_user.content_id:
        abort(403)
    past = PastBills(name=bill.name, amount=bill.amount, fixed_amt=bill.fixed_amt, due=bill.due,
                     recurring=bill.recurring, frequency=bill.frequency, category=bill.category,
                     user_id=current_user.id)
    if bill.recurring:
        adder = frequency.get(bill.frequency)
        if adder == 7 or adder == 14:
            bill.due = bill.due.replace(day=bill.due.day + adder)
        elif adder == 0:
            db.session.delete(bill)
        else:
            bill.due = bill.due.replace(month=bill.due.month + adder)
    else:
        db.session.delete(bill)
    db.session.add(past)
    db.session.commit()
    return redirect(url_for('bills.bill_index'))


@bills.route("/past_bills")
@login_required
def past_bills():
    bills = PastBills.query.filter_by(user_id=current_user.id).order_by(PastBills.due)
    return render_template('bill_templates/past_bills.html', title='Past Bills', bills=bills)


@bills.route("/bill/<int:bill_id>/delete_past_bill", methods=['POST'])
@login_required
def delete_past_bill(bill_id):
    bill = PastBills.query.get_or_404(bill_id)
    if bill.user_id != current_user.content_id:
        abort(403)
    db.session.delete(bill)
    db.session.commit()
    flash('Bill has been removed successfully', 'success')
    return redirect(url_for('bills.past_bills'))
