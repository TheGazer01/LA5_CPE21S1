# Payment System (Polymorphism)

## pip modules used
| Module        | Used for                                   |
|---------------|--------------------------------------------|
| ttkbootstrap  | Modern themed tkinter widgets (GUI)        |
| qrcode        | QR code for each successful payment        |
| Pillow        | Displays the QR code image inside tkinter  |
| reportlab     | Exports a PDF receipt                      |
| rich          | Banner and summary table in the console    |

## Setup
    pip install -r requirements.txt
    # or install the whole package:
    pip install .

## Run
    python main.py            # tkinter GUI
    python main.py --cli      # console demo
    python -m payment_system  # GUI
    payment-system            # GUI (after `pip install .`)

tkinter ships with Python on Windows/macOS. On Ubuntu/Debian: `sudo apt install python3-tk`.
