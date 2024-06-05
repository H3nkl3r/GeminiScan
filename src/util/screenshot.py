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
        return total_width, total_height

    def close(self):
        # Close the browser
        self.driver.quit()


def get_thumbnail_for_llava(path: str):
    # Load the image
    image = Image.open(path)

    # Resize the image in place
    image.thumbnail((667, 336))

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

    # The width for each image is assumed to be max 667 pixels and the height 336 pixels
    # 10 pixels are reserved for the black line in the middle
    new_width = 667 * 2 + 10
    new_height = 336
    new_image = Image.new('RGB', (new_width, new_height), "black")  # Create a new black image to ensure the entire area is filled

    # Calculate the starting x-coordinate for image2 to leave a 10-pixel black line
    image2_start_x = 667 + 10

    # Paste image1 on the left
    new_image.paste(image1, (0, 0))

    # Paste image2 on the right, starting after the 10-pixel gap
    new_image.paste(image2, (image2_start_x, 0))

    # Save the resulting image to the provided path
    new_image.save(save_path)

    return save_path
    
def concat_images_with_line_full_res(img1_path, img2_path, save_path: str):
    # Open the images
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    # Determine the new width and height
    new_width = img1.width + img2.width + 10
    new_height = max(img1.height, img2.height)

    # Create a new image with the new dimensions, filled with black
    new_img = Image.new('RGB', (new_width, new_height), "black")

    # Paste the first image
    new_img.paste(img1, (0, 0))

    # Paste the second image, offset by the width of the first image + 10 pixels
    new_img.paste(img2, (img1.width + 10, 0))

    # Save the resulting image to the provided path
    new_img.save(save_path)

    return save_path

