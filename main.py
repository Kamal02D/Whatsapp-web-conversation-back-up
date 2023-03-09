# -*- coding: utf-8 -*-
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd
from enum import Enum
from selenium.webdriver.common.action_chains import ActionChains



##### todo: you might need to change some of these to make this project work for you

CSV_FILE_STORING_LOCATION = r"C:\Users\user\Desktop\xyz.csv"
CHROME_DATA_LOCATION = r"C:\Users\user\AppData\Local\Google\Chrome\User Data"
PROFILE_NAME = "Default"

class ConversationType(Enum):
    GROUPE = "group"
    INDIVIDUAL = "individual"


def loadWhatsapp():
    """this function loads the whatsapp web app and waits until all the conversations are loaded"""
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir="+CHROME_DATA_LOCATION)
    options.add_argument(r"--profile-directory="+PROFILE_NAME)
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    driver.get("https://web.whatsapp.com")
    while True:
        try:
            driver.find_element(By.CLASS_NAME,
                                "_3WByx")  # trying to find the div that contains the profile photo if it's not there then the page is not yet loaded
            break
        except:
            pass
        time.sleep(0.5)
    print("loaded !!")
    return driver


def read_divs(driver):
    """reads the messages that are currently on the screen"""
    container = driver.find_element(By.ID, "pane-side")
    divs = container.find_elements(By.CLASS_NAME, "rx9719la")
    return divs


def print_msgs(divs):
    """takes the divs of class rx9719la and print them"""
    for div in divs:
        title = div.find_element(By.CLASS_NAME, "_21S-L").find_element(By.TAG_NAME, "span").get_attribute("title")
        print(title)


def getConversations_count(driver):
    elem = driver.find_element(By.CLASS_NAME, "_3YS_f")
    return int(elem.get_attribute("aria-rowcount"))


def sort_divs(divs):
    """sort the divs that contains the conversations"""
    # the divs seems to be not sorted, so we should sort them
    transform_values = []  # the divs seems to be sorted using a property called transform when the lowest value appears first for example a div with transform: translateY(165px) should appear before a div with transform: translateY(190px)
    for div in divs:
        trans_val = div.get_attribute("style").split(";")[-2].split(":")[-1]
        trans_val = int(re.findall(r'\d+', trans_val)[0])
        transform_values.append(trans_val)
    transform_values.sort()
    new_divs = [None for _ in divs]
    for div in divs:
        trans_val = div.get_attribute("style").split(";")[-2].split(":")[-1]
        trans_val = int(re.findall(r'\d+', trans_val)[0])
        new_divs[transform_values.index(trans_val)] = div
    return new_divs


def scroll(driver, divs_count):
    """scrolls into the last element of the divs"""
    driver.execute_script(
        f"document.getElementById('pane-side').scroll(0,{72 * (divs_count - 1)})")  # 72 is the height of each row


def get_msg_divs(driver):
    msg_divs_1 = driver.find_elements(By.CLASS_NAME, "message-out")
    msg_divs_2 = driver.find_elements(By.CLASS_NAME, "message-in")
    if len(msg_divs_1) != 0 and len(msg_divs_2) != 0:
        if msg_divs_2[0].location["y"] * -1 > msg_divs_1[0].location["y"] * -1:
            return msg_divs_2 + msg_divs_1
    return msg_divs_1 + msg_divs_2


def is_a_text_msg(div):
    try:
        div.find_element(By.CLASS_NAME, "_21Ahp").find_element(By.CLASS_NAME, "_11JPr")
        return True
    except:
        return False


def get_one_msg_data(div, other_name, other_num, conversation_type , old_name):
    """returns message , date and time , conversation type ,group title, sender , receiver , sender number , receiver number"""
    # not all the fields are entered for example the group title is only available  when the conversation type is group
    # sender/receiver one of these is entered and the other one not
    # when sender and receiver are empty that means that the message is sent by me in group
    # print(div.get_attribute("outerHTML"))
    # print(old_name)
    msg = div.find_element(By.CLASS_NAME, "_21Ahp").find_element(By.CLASS_NAME, "_11JPr").text
    date_time_divs = div.find_elements(By.CLASS_NAME, "copyable-text")
    date = None
    group_member_name = ""
    group_member_number = ""
    for d_div in date_time_divs:
        try:
            # print("dcd")
            t = d_div.get_attribute("data-pre-plain-text")
            # print("f  :", t)
            h, m, mon, day, ye, group_member = re.search(r'\[(\d+):(\d+), (\d+)/(\d+)/(\d+)] (.+):', t).groups()
            # whatsapp uses the usa timing which has one problem is that 00:00 is 24:00
            if h == "24":
                h = "00"
            date = datetime.strptime(f'{ye}-{mon}-{day} {h}-{m}', '%Y-%m-%d %H-%M')
            # print("date : ", date)
            try:
                group_member_name = div.find_element(By.CLASS_NAME, "_2ne0X")
                father_role = group_member_name.find_element(By.XPATH, "./..").get_attribute("role")
                if father_role == "button":  # when it's a reply
                    raise Exception("dd")
                group_member_name = group_member_name.text
                group_member_number = group_member
            except:
                group_member_name = group_member
                group_member_number = "+" + div.get_attribute("data-id").split("@")[1].split("_")[-1]
                # add spacing
                tree, els = re.search(r"\+(\d{3})(.+)", group_member_number).groups()
                group_member_number = re.sub(r"\+(\d+)(.+)", f"+{tree} {els}", group_member_number)
            break
        except:
            pass
    if date is None:
        print(f"some thing went wrong : date and time are empty for {div.get_attribute('outerHTML')}")
        return None
    classes = div.get_attribute("class")
    if "message-in" in classes:
        if conversation_type == ConversationType.INDIVIDUAL:
            return [msg, date, conversation_type.value, None, other_name, None, other_num, None]
        else:
            try:
                div.find_element(By.CSS_SELECTOR , "div._6rIWC._1yJoL")
                return [msg, date, conversation_type.value, other_name, group_member_name, None, group_member_number, None]
            except:
                return [msg, date, conversation_type.value, other_name, old_name, None, group_member_number, None]
    elif "message-out" in classes:
        if conversation_type == ConversationType.INDIVIDUAL:
            return [msg, date, conversation_type.value, None, None, other_name, None, other_num]
        else:
            return [msg, date, conversation_type.value, other_name, None, None, None, None]
    else:
        print("expected error the message not sent nor received")
        exit(1)


def get_name_num(driver):
    try:
        side_bar = driver.find_element(By.CSS_SELECTOR, "section.tvf2evcx.oq44ahr5.lb5m6g5c.s9fl9ege")
        divs = side_bar.find_elements(By.CLASS_NAME, "qfejxiq4")  # business acc
        is_business_acc = False
        for div in divs:
            sub_divs = div.find_elements(By.TAG_NAME , "div")
            for sub_div in sub_divs:
                if sub_div.get_attribute("role") == "button" and sub_div.get_attribute("data-testid") == "business-action forward":
                    is_business_acc = True
        if not is_business_acc:
            raise Exception("not a business account")
        name = side_bar.find_element(By.CSS_SELECTOR, "div.p6nhtbpp.enbbiyaj.tkq7s68q.tt8xd2xn.jnwc1y2a.inww9tbj.svoq16ka").text
        number = side_bar.find_element(By.CSS_SELECTOR, "div.gx1rr48f._3VUan").text
        return name, number, ConversationType.INDIVIDUAL
    except:
        try:
            num_name = driver.find_element(By.CLASS_NAME, "b8cdf3jl").find_element(By.CLASS_NAME, "l7jjieqr").text
            try:
                name_num = driver.find_element(By.CLASS_NAME, "b8cdf3jl").find_element(By.CLASS_NAME, "a4ywakfo").text
            except:
                name_num = "~UNDEFINED BY THE USER"
            if "~" in name_num:
                return name_num[1:], num_name, ConversationType.INDIVIDUAL
            else:
                return num_name, name_num, ConversationType.INDIVIDUAL
        except:
            divs = driver.find_element(By.CLASS_NAME, "b8cdf3jl").find_element(By.CLASS_NAME, "_3RN1i").find_elements(
                By.TAG_NAME, "div")
            for div in divs:
                n = div.get_attribute("data-testid")
                if n == "group-info-drawer-subject-input":
                    return div.text, None, ConversationType.GROUPE
            print("unexpected error the group name was not found")
            exit(13)


def extract_data(all_msgs, name, num, conversation_type):
    res = []
    old_name = None
    for div in all_msgs:
        try:
            old_name = div.find_element(By.CSS_SELECTOR, "div._6rIWC._1yJoL").find_element(By.TAG_NAME , "span").text
        except:
            print(f"old name was not found in {div.get_attribute('outerHTML')}")
        if is_a_text_msg(div):
            one = get_one_msg_data(div, name, num, conversation_type, old_name)
            if one is not None:
                res.append(one)
    return res


def scroll_msg(element, driver):
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()


def end_reached(last):
    if len(last) <= 5:
        return False
    if last[-1] == last[-2] == last[-3] == last[-4]:
        return True
    return False


def getOneConversation(driver):
    all_msgs = None
    last = []
    driver.find_element(By.CLASS_NAME, "_23P3O").click()
    time.sleep(5)
    i = 0
    while True:
        all_msgs = get_msg_divs(driver)
        if len(all_msgs) == 0:
            return None
        last.append(all_msgs[0].get_attribute("data-id"))
        if end_reached(last):
            break
        # if i == 0:
        #     break
        scroll_msg(all_msgs[0], driver)
        time.sleep(3)
    name, num, convrsation_type = get_name_num(driver)
    # print(name,num)
    res = extract_data(all_msgs, name, num, convrsation_type)
    return res


def save_as_csv(data):
    csv = pd.DataFrame(
        columns=["message", "date and time", "conversation type", "group title", "sender", "receiver", "sender number",
                 "receiver number"],
        data=data,
        index=None
    )
    csv = csv.sort_values(by=["date and time"])
    csv = csv[csv.message != ""]
    csv.to_csv(CSV_FILE_STORING_LOCATION, encoding="utf-8-sig")


def insert_data(data, all_divs, divs,driver):
    """ this function scrapes every conversation and insert its data into : 1 travers all divs 2 check if already added """
    for div in divs:
        sub_div_html = div.find_element(By.CLASS_NAME, "_8nE1Y").get_attribute("innerHTML")
        if not (sub_div_html in all_divs):
            # clicking on the conversation
            print("------------->", sub_div_html)
            div.click()
            res = getOneConversation(driver)
            if res is not None:
                data.extend(res)
            all_divs.append(sub_div_html)
            print(f"{len(all_divs)}")
    return all_divs, data


def getConversations(driver):
    count = int(driver.find_element(By.CLASS_NAME, "_2A1R8").get_attribute("aria-rowcount"))
    count -= 1 # the bar that contains the photo is also count, so it does not count
    print(count)
    all_divs = []
    data = []
    while len(all_divs) != count:
        divs = read_divs(driver)
        # sort the data
        divs = sort_divs(divs)
        all_divs, data = insert_data(data, all_divs, divs,driver)
        scroll(driver, len(all_divs))
    save_as_csv(data)
    print(f"done !!!! : {len(all_divs)}")


def run():
    driver = loadWhatsapp()
    getConversations(driver)
    time.sleep(100)


if __name__ == '__main__':
    run()
