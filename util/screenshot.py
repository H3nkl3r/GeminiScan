import os

from PIL import Image, ImageDraw

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ScreenshotTaker:
    def __init__(self):
        # Setup the Chrome driver options
        options = Options()
        options.add_argument('--headless')  # Run in headless mode, no UI
        options.add_argument('--no-sandbox')  # Bypass OS security model
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

        # Instantiate the Chrome driver
        self.driver = webdriver.Chrome(options=options)

    def take_screenshot(self, html_relative_path, screenshot_path):
        # Construct the full path to the HTML file
        html_file = os.path.join(os.getcwd(), html_relative_path)

        # Load the HTML file
        self.driver.get(f"file:///{html_file}")

        # Get the size of the entire page
        total_width = self.driver.execute_script("return document.body.scrollWidth")
        total_height = self.driver.execute_script("return document.body.scrollHeight") +5

        # Set the window size to the size of the entire page
        self.driver.set_window_size(total_width, total_height)

        # Save the screenshot to the specified path
        self.driver.save_screenshot(screenshot_path)

    def close(self):
        # Close the browser
        self.driver.quit()


def get_thumbnail_for_llava(path: str):
    # Load the image
    image = Image.open(path)

    # Resize the image in place
    image.thumbnail((672, 336))

    # Extract directory and file parts
    dirname = os.path.dirname(path)
    filename_with_extension = os.path.basename(path)
    filename_without_extension, file_extension = os.path.splitext(filename_with_extension)

    # Construct the new file path
    save_to_path = os.path.join(dirname, f"{filename_without_extension}_thumbnail{file_extension}")

    # Save the thumbnail
    image.save(save_to_path)

    # Return the new file path for further use
    return save_to_path


def concat_images_with_line(image_path1: str, image_path2: str, save_path: str):
    # Open the images
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    # Resize images to have the same height if necessary
    if image1.height != image2.height:
        new_height = min(image1.height, image2.height)
        image1 = image1.resize((int(image1.width * new_height / image1.height), new_height), Image.ANTIALIAS)
        image2 = image2.resize((int(image2.width * new_height / image2.height), new_height), Image.ANTIALIAS)

    # Create a new image with a width equal to the sum of both images and a small gap for the line
    total_width = image1.width + image2.width
    new_image = Image.new('RGB', (total_width, image1.height))

    # Paste image1 on the left
    new_image.paste(image1, (0, 0))

    # Paste image2 on the right
    new_image.paste(image2, (image1.width + 1, 0))

    # Draw a black line between the images
    draw = ImageDraw.Draw(new_image)
    line_x = image1.width - 6
    draw.line((line_x, 0, line_x, image1.height), fill='black', width=10)

    # Save the resulting image to the provided path
    new_image.save(save_path)

    return save_path  # Optionally return the path to the saved image
