import json
import os
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time

REPO_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"

def generate_invoice(month, year):
    with open("internet_bill.html", "r") as file:
        data = file.read()

    # format string with provided name parameter
    name = "John Doe"
    address_line_1 = "Flat No. 123, Tower A, Prestige Tech Park"
    address_line_2 = ""
    address_line_3 = "Kadubeesanahalli, Panathur Main Road"
    city = "Bangalore"
    state = "Karnataka"
    pincode = "560103"
    billing_month = month[:3] + ", " + str(year)
    amount_payable = "7,999.9"
    amount_after_due_date = "8,099.9"
    cgst = "610.16"
    sgst = "610.16"
    total_charges = "6,779.57"
    total_tax = "1220.32"
    phone_number = "9876543210"
    invoice_number = str(randint(100000000, 999999999))
    last_day_of_month = (
        datetime.strptime(("01/" + month[:3].lower() + "/" + str(year)), "%d/%b/%Y")
        + timedelta(days=32)
    ).replace(day=1) - timedelta(days=1)
    from_date = (last_day_of_month - timedelta(
        days=(last_day_of_month.day - 1)
    )).strftime("%d/%m/%Y")
    due_date = (last_day_of_month - timedelta(days=15)).strftime("%d/%m/%Y")
    invoice_date = from_date
    to_date = last_day_of_month.strftime("%d/%m/%Y")
    number_of_days = str(last_day_of_month.day)
    transaction_date = (
        str(randint(1, last_day_of_month.day))
        + "/"
        + month[:3].lower()
        + "/"
        + str(year)
    )
    payment_reference_number = str(randint(1000000000, 9999999999))

    # find the placeholder and replace it with the name
    data = data.replace("{name}", name)
    data = data.replace("{ADDRESS_LINE_1}", address_line_1)
    data = data.replace("{ADDRESS_LINE_2}", address_line_2)
    data = data.replace("{ADDRESS_LINE_3}", address_line_3)
    data = data.replace("{CITY}", city)
    data = data.replace("{STATE}", state)
    data = data.replace("{PINCODE}", pincode)
    data = data.replace("{BILLING_MONTH}", billing_month)
    data = data.replace("{INVOICE_DATE}", invoice_date)
    data = data.replace("{AMOUNT_PAYABLE}", amount_payable)
    data = data.replace("{DUE_DATE}", due_date)
    data = data.replace("{AMOUNT_AFTER_DUE_DATE}", amount_after_due_date)
    data = data.replace("{CGST}", cgst)
    data = data.replace("{SGST}", sgst)
    data = data.replace("{TOTAL_CHARGES}", total_charges)
    data = data.replace("{TOTAL_TAX}", total_tax)
    data = data.replace("{PHONE_NUMBER}", phone_number)
    data = data.replace("{INVOICE_NUMBER}", invoice_number)
    data = data.replace("{FROM_DATE}", from_date)
    data = data.replace("{TO_DATE}", to_date)
    data = data.replace("{NUMBER_OF_DAYS}", number_of_days)
    data = data.replace("{TRANSACTION_DATE}", transaction_date)
    data = data.replace("{PAYMENT_REFERENCE_NUMBER}", payment_reference_number)

    # save the modified HTML to a new file
    new_file = "temp.html"

    with open("temp.html", "w") as file:
        file.write(data)

    # Path to save the PDF file
    pdf_file = "files/" + month + "_" + str(year) + ".pdf"

    # Convert HTML to PDF
    html_to_pdf(new_file, pdf_file)


def html_to_pdf(html_file, pdf_file):
    # Configure Chrome options
    chrome_options = Options()

    prefs = {
        "printing.print_preview_sticky_settings.appState": json.dumps(
            {
                "recentDestinations": [
                    {
                        "id": "Save as PDF",
                        "origin": "local",
                        "account": "",
                    }
                ],
                "selectedDestinationId": "Save as PDF",
                "version": 2,
            }
        ),
        "savefile.default_directory": REPO_PATH,
        "download.default_directory": REPO_PATH,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--kiosk-printing")

    # Create a new instance of Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load HTML file
        driver.get("file://" + REPO_PATH + html_file)

        # Save page as PDF
        driver.execute_script("window.print();")

        # Rename the default downloaded PDF to the desired name
        os.rename(REPO_PATH + html_file + ".pdf", REPO_PATH + pdf_file)

        # delete the temp.html file
        os.remove(REPO_PATH + html_file)

    finally:
        # Close the browser
        driver.quit()


if __name__ == "__main__":
    calendar_start_year = 2023
    calendar_end_year = 2024

    billingMonths = {
        calendar_start_year: [
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        calendar_end_year: ["January", "February", "March"],
    }

    # iterate over the key value pairs of the months dictionary
    for year, month_list in billingMonths.items():
        for month in month_list:
            generate_invoice(month, year)
            time.sleep(5)