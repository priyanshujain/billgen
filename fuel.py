import imgkit
import random
import os
import shutil

from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageEnhance, ImageFilter
import random
from datetime import datetime, timedelta


def old_photo_effect(
    image_path, output_path, noise_level=0.2, brightness_factor=1.0, contrast_factor=1.0
):
    # Open the image
    img = Image.open(image_path)

    # Apply noise
    noisy_img = add_noise(img, noise_level)

    # Add random artifacts
    noisy_img = add_artifacts(noisy_img)

    # Add weird edges
    noisy_img = add_weird_edges(noisy_img)

    # Add folded paper effect
    noisy_img = add_folded_paper_effect(noisy_img, num_folds=30)

    # Adjust brightness and contrast
    enhancer = ImageEnhance.Brightness(noisy_img)
    noisy_img = enhancer.enhance(brightness_factor)
    enhancer = ImageEnhance.Contrast(noisy_img)
    noisy_img = enhancer.enhance(contrast_factor)

    # Apply sepia tone
    noisy_img = apply_sepia(noisy_img)

    # Save the result
    noisy_img.save(output_path)


def add_noise(image, noise_level):
    width, height = image.size
    pixels = image.load()
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            noise = random.randint(-int(noise_level * 255), int(noise_level * 255))
            pixels[x, y] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise)),
            )
    return image


def apply_sepia(image):
    sepia = image.convert("L")
    sepia = sepia.filter(ImageFilter.SMOOTH)
    sepia = sepia.filter(ImageFilter.SHARPEN)
    sepia = sepia.convert("RGB")
    return sepia


def add_artifacts(image, num_artifacts=1000):
    width, height = image.size
    pixels = image.load()
    for _ in range(num_artifacts):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        r, g, b = pixels[x, y]
        # Introduce random artifacts (e.g., stains, discoloration)
        pixels[x, y] = (
            max(0, min(255, r + random.randint(-50, 50))),
            max(0, min(255, g + random.randint(-50, 50))),
            max(0, min(255, b + random.randint(-50, 50))),
        )
    return image


def add_weird_edges(image):
    width, height = image.size
    pixels = image.load()
    # Create weird edges by modifying pixel values near the edges
    for x in range(width):
        for y in range(height):
            if x < 20 or x > width - 20 or y < 20 or y > height - 20:
                # Add random color variation to edge pixels
                pixels[x, y] = (
                    max(0, min(255, pixels[x, y][0] + random.randint(-50, 50))),
                    max(0, min(255, pixels[x, y][1] + random.randint(-50, 50))),
                    max(0, min(255, pixels[x, y][2] + random.randint(-50, 50))),
                )
    return image


def add_folded_paper_effect(image, num_folds=3):
    width, height = image.size
    pixels = image.load()
    for _ in range(num_folds):
        # Generate random points for the start and end of a fold line
        x1 = random.randint(0, width - 1)
        y1 = random.randint(0, height - 1)
        x2 = random.randint(0, width - 1)
        y2 = random.randint(0, height - 1)
        # Draw the fold line by changing pixel values along the line
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if (x - x1) * (y2 - y1) == (y - y1) * (x2 - x1):
                    pixels[x, y] = (
                        max(0, min(255, pixels[x, y][0] - 50)),
                        max(0, min(255, pixels[x, y][1] - 50)),
                        max(0, min(255, pixels[x, y][2] - 50)),
                    )
    return image


def generate_invoice(date: str, id: int):
    # Step 1: Open and read the HTML file
    file_loader = FileSystemLoader(
        "templates"
    )  # Assuming your HTML file is in a directory named 'templates'
    env = Environment(loader=file_loader)

    # Step 2: Load the template
    template = env.get_template(
        "fuel_bill.html"
    )  # Assuming your HTML file is named 'index.html'

    # Step 3: Render the template with data

    # rate is rate of fuel per litre is random float between 108 and 110
    rate = random.uniform(108, 110)
    rate_str = "{:.2f}".format(rate)

    amount = random.uniform(3000, 4000)
    amount_str = "{:.2f}".format(amount)

    volume = amount / rate
    volume_str = "{:.2f}".format(volume)

    # time is random time between 8:00am and 2am in 24 hour format
    hour = random.randint(8, 23)
    minute = random.randint(0, 59)

    time = "{:02d}:{:02d}".format(hour, minute)
    receipt_number = random.randint(1000, 9999)
    context = {
        "rate": rate_str,
        "amount": amount_str,
        "volume": volume_str,
        "date": date,
        "time": time,
        "receipt_number": receipt_number,
    }
    output = template.render(context)

    imgkit.from_string(output, "out.jpg", options={"format": "jpg", "width": 320})
    old_photo_effect("out.jpg", "out.jpg")

    # rename the file to the date
    newFile = str(id) + "_" + date + ".jpg"
    newFile = newFile.replace("/", "")
    if not os.path.exists(newFile):
        _ = open(newFile, "w")
    os.rename("out.jpg", newFile)
    basePath = os.path.dirname(os.path.abspath(__file__))
    opPath = basePath + "/files/fuel/"
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
        interval = random.randint(7, 15)
        # Create bill details
        # check if counter is divisible by 5
        # if counter % 5 != 0:
        #     dt = current_date

        # if counter % 15 == 0:
        #     bill_dates.append({"date": dt.strftime("%d/%m/%Y"), "id": counter})
        #     counter += 1
        #     current_date += timedelta(days=interval)
        dt  = current_date

        bill = {"date": dt.strftime("%d/%m/%Y"), "id": counter}

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
        generate_invoice(date, bill_date["id"])
