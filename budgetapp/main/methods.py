from datetime import datetime
from flask_googlecharts import PieChart
from flask_login import current_user

from budgetapp.models import Bill, PastBills
from budgetapp import charts, db


def get_chart_labels():
    return ["Subscriptions", "Rent/Mortgage", "Utilities", "Payment Plans", "Other"]


def get_chart_values():
    return [get_sum_total("subscription"), get_sum_total("rentMortgage"),
            get_sum_total("utility"), get_sum_total("pmtPlan"), get_sum_total("other")]


def get_chart_colors():
    return ["#ff404c", "#43e0f2", "#ffdf46", "#84de02", "#a020f0"]


def get_sum_total(category):
    bills = Bill.query.filter_by(user=current_user, category=category)
    past_bills = PastBills.query.filter_by(user_id=current_user.id, category=category)
    sum = 0
    for bill in bills:
        sum += bill.amount
    for bill in past_bills:
        sum += bill.amount
    return sum


def move_paid():
    bills = Bill.query.order_by(Bill.due)
    current_day = datetime.now()
    frequency = {"once": 0, "weekly": 7, "bi-weekly": 14, "monthly": 1, "bi-monthly": 2, "yearly": 12}
    for bill in bills:
        if bill.due.day < current_day.day and bill.due.month <= current_day.month:
            past = PastBills(name=bill.name, amount=bill.amount, fixed_amt=bill.fixed_amt, due=bill.due,
                             recurring=bill.recurring, frequency=bill.frequency, category=bill.category,
                             user_id=bill.user_id)
            if bill.recurring:
                adder = frequency.get(bill.frequency)
                if adder is None or adder == 0:
                    db.session.delete(bill)
                elif adder == 7 or adder == 14:
                    bill.due = bill.due.replace(day=bill.due.day + adder)
                else:
                    if bill.due.month >= 12:
                        bill.due.replace(month=1)
                    else:
                        bill.due = bill.due.replace(month=bill.due.month + adder)
            else:
                db.session.delete(bill)
        else:
            break
        db.session.add(past)
        db.session.commit()


def time_greeting():
    current_time = datetime.now()
    greeting = "Hello,"
    if current_time.hour < 12:
        greeting = "Good Morning,"
    elif current_time.hour < 17:
        greeting = "Good Afternoon,"
    elif current_time.hour >= 17:
        greeting = "Good Evening,"
    return greeting
