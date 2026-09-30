import tkinter as tk
from tkinter import messagebox
from payments.cash import CashPayment
from payments.gcash import GCashPayment
from payments.credit_card import CreditCardPayment
from payments.bank_transfer import BankTransferPayment

window = tk.Tk()
window.title("Payment System")
window.geometry("500x500")

title_label = tk.Label(
    window,
    text="PAYMENT SYSTEM", font=("Arial", 20, "bold")
)
title_label.pack(pady=20)

amount_label = tk.Label(
    window,
    text="Enter Payment Amount:"
)
amount_label.pack()

amount_entry = tk.Entry(
    window,
    width=30
)
amount_entry.pack(pady=10)

def process_payment(payment):
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            messagebox.showerror(
                "Invalid Amount",
                "Please enter an amount greater than zero."
            )
            return
        result = payment.pay(amount)
        messagebox.showinfo( "Payment Successful",
            result
        )
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid amount."
        )

button_frame = tk.Frame(window)
button_frame.pack(pady=20)

cash_button = tk.Button(
    button_frame,
    text="Pay with Cash",
    width=25,
    command=lambda:
process_payment(CashPayment())
)
cash_button.grid(
    row=0,
    column=0,
    padx=10,
    pady=5
)

gcash_button = tk.Button(
    button_frame,
    text="Pay with GCash",
    width=25,
    command=lambda:
process_payment(GCashPayment()))
gcash_button.grid(
    row=1,
    column=0,
    padx=10,
    pady=5
)

card_button = tk.Button(
    button_frame,
    text="Pay with Credit Card",
    width=25,
    command=lambda:
process_payment(CreditCardPayment())
)
card_button.grid(
    row=2,
    column=0,
    padx=10,
    pady=5
)

bank_button = tk.Button(
    button_frame,
    text="Pay with Bank Transfer",
    width=25,
    command=lambda:
process_payment(BankTransferPayment())
)
bank_button.grid(
    row=3,
    column=0,
    padx=10,
    pady=5
)

exit_button = tk.Button(
    window,
    text="Exit",
    width=25,
    command=window.destroy
)
exit_button.pack(pady=20)

window.mainloop()