import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import ttkbootstrap as ttk
from PIL import ImageTk

from payments import (
    CashPayment,
    EWalletPayment,
    CreditCardPayment,
    DebitCardPayment,
    BankTransferPayment,
)
from utils.icons import make_icon
from utils.qr import make_qr
from utils.formatting import php
from utils.receipt import make_receipt_pdf
from utils.report import export_csv, show_chart
from utils.console import log_payment, show_history

BUSINESS_NAME = "My Business"
BLUE = "#1a56db"

history = []
last_receipt = {}
selected = {"name": None, "class": None}

window = ttk.Window(themename="cosmo")
window.title(BUSINESS_NAME)
window.geometry("680x780")
window.minsize(640, 720)
window.configure(background=BLUE)

style = ttk.Style()
style.configure("Blue.TFrame", background=BLUE)
style.configure("Blue.TLabel", background=BLUE, foreground="white")
style.configure("Card.TFrame", background="white")
style.configure("Card.TLabel", background="white", foreground="#1f2937")
style.configure("Card.TLabelframe", background="white", bordercolor="#c9ced6")
style.configure("Card.TLabelframe.Label", background="white", foreground="#1f2937",
                font=("Segoe UI", 9))

header = ttk.Frame(window, style="Blue.TFrame")
header.pack(side="top", pady=(20, 12))
ttk.Label(header, text=BUSINESS_NAME.upper(), style="Blue.TLabel",
          font=("Segoe UI", 22, "bold")).pack()
ttk.Label(header, text="Payment System", style="Blue.TLabel",
          font=("Segoe UI", 10)).pack()

footer = ttk.Frame(window, style="Blue.TFrame")
footer.pack(side="bottom", fill="x", padx=20, pady=15)

card = ttk.Frame(window, style="Card.TFrame", padding=15)
card.pack(side="top", fill="both", expand=True, padx=20)

# ---------------------------------------------------------------- Payment Details
details = ttk.Labelframe(card, text="Payment Details", style="Card.TLabelframe", padding=15)
details.pack(fill="x")
details.columnconfigure(1, weight=1)

ttk.Label(details, text="Payer name", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=5)
name_entry = ttk.Entry(details)
name_entry.grid(row=0, column=1, sticky="ew", padx=(15, 0), pady=5)

ttk.Label(details, text="Amount due (PHP)", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=5)
amount_entry = ttk.Entry(details)
amount_entry.grid(row=1, column=1, sticky="ew", padx=(15, 0), pady=5)

ttk.Label(details, text="Payment method", style="Card.TLabel").grid(row=2, column=0, sticky="nw", pady=8)
method_frame = ttk.Frame(details, style="Card.TFrame")
method_frame.grid(row=2, column=1, sticky="ew", padx=(15, 0))
for column in range(3):
    method_frame.columnconfigure(column, weight=1, uniform="method")

ttk.Label(details, text="Cash tendered", style="Card.TLabel").grid(row=3, column=0, sticky="w", pady=5)
cash_entry = ttk.Entry(details)
cash_entry.grid(row=3, column=1, sticky="ew", padx=(15, 0), pady=5)

action_frame = ttk.Frame(details, style="Card.TFrame")
action_frame.grid(row=4, column=0, columnspan=2, sticky="e", pady=(10, 0))

# ---------------------------------------------------------------- Latest Receipt
receipt_box = ttk.Labelframe(card, text="Latest Receipt", style="Card.TLabelframe", padding=10)
receipt_box.pack(fill="x", pady=(12, 0))

qr_holder = ttk.Frame(receipt_box, style="Card.TFrame", width=120, height=120)
qr_holder.pack(side="left", padx=(0, 15))
qr_holder.pack_propagate(False)
qr_label = ttk.Label(qr_holder, text="No QR yet", style="Card.TLabel",
                     foreground="#9ca3af", anchor="center")
qr_label.pack(expand=True)

receipt_info = ttk.Frame(receipt_box, style="Card.TFrame")
receipt_info.pack(side="left", fill="both", expand=True)
receipt_label = ttk.Label(receipt_info, style="Card.TLabel", justify="left", wraplength=400,
                          text="Make a successful payment to generate a QR code and receipt.")
receipt_label.pack(anchor="w")

# ---------------------------------------------------------------- Transaction Log
log_box = ttk.Labelframe(card, text="Transaction Log", style="Card.TLabelframe", padding=8)
log_box.pack(fill="both", expand=True, pady=(12, 0))

log_scroll = ttk.Scrollbar(log_box, orient="vertical")
log_scroll.pack(side="right", fill="y")
log_text = tk.Text(log_box, height=5, wrap="word", state="disabled", relief="solid",
                   borderwidth=1, font=("Consolas", 9), yscrollcommand=log_scroll.set)
log_text.pack(side="left", fill="both", expand=True)
log_scroll.configure(command=log_text.yview)


def add_log(line):
    log_text.configure(state="normal")
    log_text.insert("end", line + "\n")
    log_text.see("end")
    log_text.configure(state="disabled")


def show_receipt(result):
    qr_image = ImageTk.PhotoImage(make_qr(
        f"{BUSINESS_NAME}\n{last_receipt['number']}\n{result}", 110))
    qr_label.configure(image=qr_image, text="")
    qr_label.image = qr_image

    lines = [f"Receipt No. {last_receipt['number']}", f"Payer: {last_receipt['payer']}", result]
    if last_receipt["tendered"] is not None:
        lines.append(f"Cash tendered: {php(last_receipt['tendered'])}   "
                     f"Change: {php(last_receipt['change'])}")
    receipt_label.configure(text="\n".join(lines))
    save_button.configure(state="normal")


def process_payment(payment):
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid amount."
        )
        return
    if amount <= 0:
        messagebox.showerror(
            "Invalid Amount",
            "Please enter an amount greater than zero."
        )
        return

    tendered = change = None
    if selected["name"] == "Cash":
        try:
            tendered = float(cash_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter the cash tendered."
            )
            return
        if tendered < amount:
            messagebox.showerror(
                "Insufficient Payment",
                f"Insufficient payment.\nPlease enter an amount equal to or greater than {php(amount)}."
            )
            return
        change = tendered - amount

    result = payment.pay(amount)
    history.append((payment.__class__.__name__, amount, result))
    log_payment(len(history), result)

    now = datetime.now()
    last_receipt.clear()
    last_receipt.update({
        "business": BUSINESS_NAME,
        "number": f"{len(history):06d}",
        "date": now.strftime("%B %d, %Y"),
        "time": now.strftime("%I:%M %p"),
        "payer": name_entry.get().strip() or "Walk-in Customer",
        "method": selected["name"],
        "amount": amount,
        "tendered": tendered,
        "change": change,
        "result": result,
    })

    entry = f"#{len(history)} [{last_receipt['time']}] {last_receipt['payer']}: {result}"
    if change is not None:
        entry += f" Change: {php(change)}"
    add_log(entry)
    show_receipt(result)

    for field in (name_entry, amount_entry, cash_entry):
        field.delete(0, "end")


def save_pdf():
    if not last_receipt:
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        initialfile=f"receipt_{last_receipt['number']}.pdf",
        filetypes=[("PDF file", "*.pdf")]
    )
    if path:
        make_receipt_pdf(last_receipt, path)
        messagebox.showinfo("Saved", f"Receipt saved to {path}")


def clear_log():
    if history and not messagebox.askyesno(
            "Clear log", "This also clears the payment history used by Chart and Export. Continue?"):
        return
    history.clear()
    log_text.configure(state="normal")
    log_text.delete("1.0", "end")
    log_text.configure(state="disabled")


def export():
    if not history:
        messagebox.showinfo("Nothing to Export", "Make a payment first.")
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV file", "*.csv")]
    )
    if path:
        export_csv(history, path)
        messagebox.showinfo("Exported", f"Saved to {path}")


def exit_app():
    show_history(history)
    window.destroy()


payment_methods = [
    ("Cash", CashPayment),
    ("E-Wallet", EWalletPayment),
    ("Credit Card", CreditCardPayment),
    ("Debit Card", DebitCardPayment),
    ("Bank Transfer", BankTransferPayment),
]

method_buttons = {}


def select_method(name, payment_class):
    selected["name"] = name
    selected["class"] = payment_class
    for label, button in method_buttons.items():
        button.configure(bootstyle="primary" if label == name else "primary-outline")
    cash_entry.configure(state="normal" if name == "Cash" else "disabled")


icons = []
for index, (name, payment_class) in enumerate(payment_methods):
    icon = ImageTk.PhotoImage(make_icon(name))
    icons.append(icon)
    button = ttk.Button(
        method_frame,
        text=name,
        image=icon,
        compound="left",
        bootstyle="primary-outline",
        command=lambda n=name, pc=payment_class: select_method(n, pc)
    )
    button.grid(row=index // 3, column=index % 3, sticky="ew", padx=3, pady=3, ipady=2)
    method_buttons[name] = button

ttk.Button(action_frame, text="Pay", bootstyle="success", width=10,
           command=lambda: process_payment(selected["class"]())).pack(side="left", padx=(0, 10))
ttk.Button(action_frame, text="Clear log", bootstyle="secondary-outline", width=10,
           command=clear_log).pack(side="left")

save_button = ttk.Button(receipt_info, text="Save PDF receipt", bootstyle="secondary-outline",
                         state="disabled", command=save_pdf)
save_button.pack(anchor="w", pady=(10, 0))

select_method("Cash", CashPayment)

for text, command in [
    ("Chart", lambda: show_chart(window, history)),
    ("Export", export),
    ("Exit", exit_app),
]:
    ttk.Button(footer, text=text, bootstyle="light",
               command=command).pack(side="left", expand=True, fill="x", padx=4)

window.mainloop()