import json

from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from flask_googlecharts import PieChart
from datetime import datetime

from budgetapp.main.methods import time_greeting, get_chart_labels, get_chart_values, \
    get_chart_colors, move_paid
from budgetapp.models import Bill
from budgetapp import charts

main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template('index.html')


@main.route("/dashboard")
@login_required
def dashboard():
    move_paid()
    greeting = time_greeting()
    chart_labels = get_chart_labels()
    chart_values = get_chart_values()
    chart_colors = get_chart_colors()
    user = current_user.name
    bills = Bill.query.filter_by(user=current_user).order_by(Bill.due).limit(10)
    return render_template('dashboard.html', title='Dashboard', set=zip(chart_values, chart_labels, chart_colors),
                           greeting=greeting, user=user, bills=bills)


@main.route("/spendings")
@login_required
def spendings():
    return render_template('spendings.html', title='Spendings')
