class BillSet:

    def __init__(self):
        self.bill_list = []

    def add_bill(self, bill):
        self.bill_list.append(bill)

    def avg_amount(self):
        total = 0
        for bill in range(0,len(self.bill_list)):
            total += bill.amount
        return total / len(self.bill_list)