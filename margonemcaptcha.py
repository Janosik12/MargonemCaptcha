from selenium import webdriver
from screen_search import *
import mss.tools
import cv2
import settings
import pyautogui


q1 = input('Chrome path:')
q2 = input('Driver path:')

# Chrome path is necessary to keep the chrome options so it will save your account password and number
url = "https://new.margonem.pl/"
options = webdriver.ChromeOptions()
options.add_argument(q1)
driver = webdriver.Chrome(q2, options=options)
driver.get(url)
driver.find_element_by_class_name('enter-game').click()
time.sleep(2)


# Copy the sentence that points proper solution for captcha and return image that will later get matched
def colour():
    text_colour = driver.find_element_by_class_name('captcha__question').text
    print(text_colour)
    colors = {'Niebieski': 'niebieski',
              'Biały': 'bialy',
              'Czarny': 'czarny',
              'Czerwony': 'czerwony',
              'Zielony': 'zielony',
              'Żółty': 'zolty'}
    key_lookup = None
    for key in colors.keys():
        if key in text_colour:
            key_lookup = key
            break
    return colors.get(key_lookup)


# Takes a screenshot
def image_grab():
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": settings.SCREEN_X_RESOLUTION, "height": settings.SCREEN_Y_RESOLUTION}
        return sct.grab(monitor)


# Template matching given image to previously done screenshot and returning the coords if similarity is found
def detect(image):
    img = np.array(image_grab())
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('{}.png'.format(image), cv2.IMREAD_GRAYSCALE)
    res = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    w, h = template.shape[::-1]
    loc = np.where(res >= 0.9)
    cv2.destroyAllWindows()
    try:
        return loc
    except IndexError:
        return False


while True:
    loc = detect(colour())
    if loc:
        pyautogui.click(loc[1] + 10, loc[0] + 10)
    time.sleep(2)
    driver.find_element_by_class_name('captcha__confirm').click()
