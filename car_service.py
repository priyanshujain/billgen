import imgkit
import random
import os
import shutil

from jinja2 import Environment, FileSystemLoader
import random
from datetime import datetime, timedelta



def generate_invoice(date: datetime, id: int):
    # Step 1: Open and read the HTML file
    file_loader = FileSystemLoader(
        "templates"
    )  # Assuming your HTML file is in a directory named 'templates'
    env = Environment(loader=file_loader)

    # Step 2: Load the template
    template = env.get_template(
        "car_service.html"
    )  # Assuming your HTML file is named 'index.html'

    # Step 3: Render the template with data

    # rate is rate of fuel per litre is random float between 108 and 110
    name = "John Doe"
    email = "test@test.com"
    phone = "+1234567890"
    address = "123, Test Street, Test City, Test State, 123456"
    vehicle_number = "KA01AB1234"
    vehicle_model = "Maruti Suzuki Swift"

    invoice_number = "{}-00{}".format(date.strftime("%Y%m%d"), id)
    
    context = {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "vehicle_number": vehicle_number,
        "vehicle_model": vehicle_model,
        "invoice_number": invoice_number,
        "date": date.strftime("%d/%m/%Y"),
        "due_date": (date + timedelta(days=7)).strftime("%d/%m/%Y"),
    }
    output = template.render(context)

    imgkit.from_string(output, "out.jpg", options={"format": "jpg", "width": 680})
    # rename the file to the date
    newFile = str(id) + "_" + date.strftime("%d/%m/%Y") + ".jpg"
    newFile = newFile.replace("/", "")
    if not os.path.exists(newFile):
        _ = open(newFile, "w")
    os.rename("out.jpg", newFile)
    basePath = os.path.dirname(os.path.abspath(__file__))
    opPath = basePath + "/files/carservice/"
    # move the file to the folder
    newFilePath = os.path.join(opPath, newFile)
    if not os.path.exists(newFilePath):
        _ = open(newFilePath, "w")
    shutil.move(newFile, newFilePath)


def generate_bill_dates(start_date, end_date):
    bill_dates = []
    current_date = start_date
    counter = 1
    dt = datetime(2023, 4, 1)
    while current_date < end_date:
        # Generate a random interval between 3 and 8 days
        interval = random.randint(150, 180)
        bill = {"date": current_date, "id": counter}

        # Add bill to the list
        bill_dates.append(bill)
        # Move to the next bill date
        current_date += timedelta(days=interval)
        counter += 1

    return bill_dates


if __name__ == "__main__":
    start_date = datetime(2023, 4, 10)
    end_date = datetime(2024, 3, 15)

    bill_dates = generate_bill_dates(start_date, end_date)

    # Display the generated bill dates
    for bill_date in bill_dates:
        #  20/12/2023
        date = bill_date["date"]
        generate_invoice(date, 34)
