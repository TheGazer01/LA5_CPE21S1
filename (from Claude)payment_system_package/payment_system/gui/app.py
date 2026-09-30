"""Tkinter GUI, themed with the pip module ttkbootstrap.

Other pip modules used here:
  - qrcode + Pillow : QR code shown after a successful payment
  - reportlab       : PDF receipt export
"""
import tkinter as tk
from tkinter import filedialog, messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import ImageTk

from payment_system.services import (
    PaymentProcessor,
    METHOD_REGISTRY,
    build_payment,
    make_qr_image,
    export_pdf_receipt,
)


class PaymentApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Payment System - Polymorphism Demo")
        self.geometry("640x840")
        self.minsize(600, 780)

        self.processor = PaymentProcessor(output=self.log)
        self.field_vars = []
        self.last_txn = None
        self._qr_photo = None  # keep a reference so Tk doesn't discard it

        self._build_form()
        self._build_receipt()
        self._build_log()
        self._on_method_change()

    # ---------- UI construction ----------
    def _build_form(self):
        form = ttk.Labelframe(self, text="Payment Details", padding=15)
        form.pack(fill=X, padx=15, pady=(15, 8))
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Payer name").grid(row=0, column=0, sticky=W, pady=4)
        self.payer_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.payer_var).grid(
            row=0, column=1, sticky=EW, padx=(10, 0), pady=4)

        ttk.Label(form, text="Amount due (PHP)").grid(row=1, column=0, sticky=W, pady=4)
        self.amount_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.amount_var).grid(
            row=1, column=1, sticky=EW, padx=(10, 0), pady=4)

        ttk.Label(form, text="Payment method").grid(row=2, column=0, sticky=W, pady=4)
        self.method_var = tk.StringVar(value=list(METHOD_REGISTRY)[0])
        self.method_box = ttk.Combobox(
            form, textvariable=self.method_var,
            values=list(METHOD_REGISTRY), state="readonly")
        self.method_box.grid(row=2, column=1, sticky=EW, padx=(10, 0), pady=4)
        self.method_box.bind("<<ComboboxSelected>>", self._on_method_change)

        self.dynamic = ttk.Frame(form)
        self.dynamic.grid(row=3, column=0, columnspan=2, sticky=EW, pady=(6, 0))
        self.dynamic.columnconfigure(1, weight=1)

        buttons = ttk.Frame(form)
        buttons.grid(row=4, column=0, columnspan=2, sticky=E, pady=(12, 0))
        ttk.Button(buttons, text="Pay", bootstyle=SUCCESS,
                   command=self.on_pay).pack(side=LEFT, padx=5)
        ttk.Button(buttons, text="Clear log", bootstyle=(SECONDARY, OUTLINE),
                   command=self.clear_log).pack(side=LEFT, padx=5)

    def _build_receipt(self):
        box = ttk.Labelframe(self, text="Latest Receipt", padding=10)
        box.pack(fill=X, padx=15, pady=8)

        self.qr_label = ttk.Label(box, text="No QR yet", width=22,
                                  anchor=CENTER, bootstyle=SECONDARY)
        self.qr_label.pack(side=LEFT, padx=(0, 15))

        right = ttk.Frame(box)
        right.pack(side=LEFT, fill=BOTH, expand=YES)
        self.receipt_info = ttk.Label(
            right, text="Make a successful payment to\ngenerate a QR code and receipt.",
            justify=LEFT)
        self.receipt_info.pack(anchor=W)
        self.pdf_button = ttk.Button(
            right, text="Save PDF receipt", bootstyle=PRIMARY,
            command=self.on_save_pdf, state=DISABLED)
        self.pdf_button.pack(anchor=W, pady=(12, 0))

    def _build_log(self):
        box = ttk.Labelframe(self, text="Transaction Log", padding=10)
        box.pack(fill=BOTH, expand=YES, padx=15, pady=(8, 8))
        self.text = tk.Text(box, height=10, wrap="word", state="disabled",
                            font=("Consolas", 10))
        scroll = ttk.Scrollbar(box, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        self.text.pack(side=LEFT, fill=BOTH, expand=YES)
        scroll.pack(side=RIGHT, fill=Y)

        self.status = ttk.Label(self, text="Transactions processed: 0",
                                bootstyle=INFO)
        self.status.pack(anchor=W, padx=15, pady=(0, 10))

    # ---------- behavior ----------
    def _on_method_change(self, _event=None):
        for child in self.dynamic.winfo_children():
            child.destroy()
        self.field_vars = []
        _cls, fields = METHOD_REGISTRY[self.method_var.get()]
        for row, (label, _typ) in enumerate(fields):
            ttk.Label(self.dynamic, text=label).grid(row=row, column=0, sticky=W, pady=4)
            var = tk.StringVar()
            ttk.Entry(self.dynamic, textvariable=var).grid(
                row=row, column=1, sticky=EW, padx=(10, 0), pady=4)
            self.field_vars.append(var)

    def on_pay(self):
        payer = self.payer_var.get().strip()
        try:
            if not payer:
                raise ValueError("'Payer name' is required.")
            amount = float(self.amount_var.get())
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
        except ValueError as err:
            msg = str(err)
            if msg.startswith("could not convert"):
                msg = "'Amount due' must be a valid number."
            messagebox.showerror("Invalid input", msg)
            return

        try:
            method = build_payment(
                self.method_var.get(), payer, [v.get() for v in self.field_vars])
        except ValueError as err:
            messagebox.showerror("Invalid input", str(err))
            return

        # Polymorphism: the processor just calls method.pay(amount)
        txn = self.processor.process(method, amount)
        self.status.configure(
            text=f"Transactions processed: {len(self.processor.history)}")
        self._update_receipt(txn)

    def _update_receipt(self, txn):
        if not txn.success:
            self.receipt_info.configure(
                text=f"Last payment FAILED ({txn.txn_id}).\nNo receipt was generated.")
            return
        self.last_txn = txn
        self._qr_photo = ImageTk.PhotoImage(make_qr_image(txn, box_size=4))
        self.qr_label.configure(image=self._qr_photo, text="")
        self.receipt_info.configure(
            text=(f"Txn ID:  {txn.txn_id}\nPayer:   {txn.payer}\n"
                  f"Method:  {txn.method}\nAmount:  PHP {txn.amount:,.2f}\n"
                  f"Time:    {txn.time_str}"))
        self.pdf_button.configure(state=NORMAL)

    def on_save_pdf(self):
        if not self.last_txn:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"receipt_{self.last_txn.txn_id}.pdf",
            filetypes=[("PDF files", "*.pdf")])
        if path:
            export_pdf_receipt(self.last_txn, path)
            messagebox.showinfo("Saved", f"Receipt saved to:\n{path}")

    def log(self, message):
        self.text.configure(state="normal")
        self.text.insert("end", message + "\n\n")
        self.text.see("end")
        self.text.configure(state="disabled")

    def clear_log(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")


def run():
    PaymentApp().mainloop()
