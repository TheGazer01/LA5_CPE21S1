"""Processor: relies only on the Payment interface, never on concrete types."""
from payment_system.core.transaction import Transaction


class PaymentProcessor:
    def __init__(self, output=print):
        self.history = []
        self.output = output  # print for the CLI, a GUI logger for tkinter

    def process(self, method, amount):
        message = method.pay(amount)  # polymorphic call
        txn = Transaction(
            payer=method.payer,
            method=method.__class__.__name__,
            amount=amount,
            message=message,
            success=method.last_success,
        )
        self.history.append(txn)
        self.output(message)
        return txn

    def process_all(self, methods, amount):
        return [self.process(m, amount) for m in methods]
