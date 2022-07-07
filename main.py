import requests  # requests
import re  # regex
import math  # to floor results
import threading
import time
import os

os.system("cls")

# information:
# fit 42 images per page

tag = "furry"


print("\u001b[38;5;78m-" * 40)
print(" " * 14 + "\u001b[38;5;247mRULE34 PARSER\u001b[0m")
print("\u001b[38;5;78m-" * 40 + "\n\n")

def get_ids(html_decoded_response):
    tags = re.findall("((?<=id\=\"p)\d+)", html_decoded_response)  # Basically gets the ids of each one of them

    return tags


def get_limit(_tag):
    response = requests.get(f"https://rule34.xxx/public/autocomplete.php?q={_tag}")

    if response.status_code == 200:

        result = response.json()[0]["label"]

        image_numbers = int(re.search("((?<=\s\()\d+)",
                                      result).group())

        page_numbers = math.ceil(
            image_numbers / 42)  # Gets the total of pages based from the information (rounded the result)

        print(f"\u001b[38;5;220mProcessing\u001b[0m \u001b[38;5;14m{str(page_numbers)}\u001b[0m pages | \u001b[38;5;14m{str(image_numbers)}\u001b[0m images... \u001b[38;5;92mPlease be patient, a rookie made this script.\u001b[0m")

        return page_numbers

    else:

        return 0


def get_page_information(tag, page):
    status = 201

    while status != 200:
        time.sleep(0.05)

        # print("Reboot")

        response = requests.get(f"https://rule34.xxx/index.php?page=post&s=list&tags={tag}+&pid={str(int(page) * 42)}")

        status = response.status_code

    return response.content.decode()


def save_image(id):
    image_response = requests.get(f"https://rule34.xxx/index.php?page=post&s=view&id={str(id)}")

    while image_response.status_code != 200:
        time.sleep(0.005)

        image_response = requests.get(f"https://rule34.xxx/index.php?page=post&s=view&id={str(id)}")

    try:
        link = "https://" + re.search("(?<=src\=\"https:\/\/us\.).+(?=\?)", image_response.content.decode()).group()
    except:
        link = "dummy"

    if link != "dummy":
        image_content = requests.get(link).content

        with open("P_RN/" + link.split("/")[-1], "wb") as f:
            f.write(image_content)


def save_table_func(page, save_table):
    THR_Table = []

    for i in get_ids(get_page_information(tag, page)):
        # https://rule34.xxx/index.php?page=post&s=view&id=5985054

        TH = threading.Thread(target=save_image, args=(str(i),))

        THR_Table.append(TH)

    for i in THR_Table:
        i.start()

    for i in THR_Table:
        i.join()


def get_pages(page_limit):
    pid_table = []

    threads_table = []

    for i in range(1, page_limit + 1):
        print(f"Process: \u001b[38;5;196m{str(round(i * 100 / (page_limit + 1), 3))}\u001b[0m%" + " " * 20, end="\r")

        save_table_func(i, pid_table)

    return pid_table


id_table = get_pages(get_limit(tag))
