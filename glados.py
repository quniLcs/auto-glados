# The code is referred to https://github.com/tyIceStream/GLaDOS_Checkin
# The method to get the cookie is further referred to https://blog.csdn.net/m0_48097541/article/details/122980934

import time
import os
import logging
import json

import requests
import undetected_chromedriver


def get_account(logger):
    # The first way to get account: from the environment variables
    cookie = os.getenv("GLADOS_COOKIE")
    token = os.getenv("PUSHPLUS_TOKEN")
    if cookie is not None and token is not None:
        logger.info("Have obtained account information from the environment variables.")
        return cookie, token

    # The second way to get account: from the file
    if os.path.exists("account.txt"):
        logger.info("Read the account information from account.txt.")
        with open("account.txt", "r") as account_file:
            account_text = account_file.readlines()

        cookie = account_text[0].split(': ')[1].strip()
        token = account_text[1].split(': ')[1].strip()
        return cookie, token

    else:  # The third way to get account: input
        logger.info("account.txt not found.")
        logger.info("Please input the following account information:")

        cookie = input("GLaDOS Cookie: ")
        token = input("PushPlus Token: ")

        with open("account.txt", "w") as account_file:
            account_file.write("GLADOS_COOKIE: %s\nPUSHPLUS_TOKEN: %s\n" % (cookie, token))

        logger.info("account.txt saved.")
        logger.info("Please pay attention to the safety of the file.")
        logger.info("A hyperlink to desktop is recommended.")

        return cookie, token


def glados_checkin(driver, logger):
    url = 'https://glados.rocks/api/user/checkin'
    script = """
        return function(){
        var request = new XMLHttpRequest();
        request.open('POST', '%s', false);
        request.setRequestHeader('content-type', 'application/json');
        request.send('{"token": "glados.network"}');
        return request;
        }();
        """ % url

    logger.info('Start to check in.')
    response = driver.execute_script(script)
    response = json.loads(response["response"])
    logger.info('The result is: %s.' % response["message"])
    logger.info('')

    return response["code"]


def glados_status(driver, logger):
    url = "https://glados.rocks/api/user/status"
    script = """
        return (function(){
        var request = new XMLHttpRequest();
        request.open('GET', '%s', false);
        request.send();
        return request;
        })();
        """ % url

    logger.info('Start to check the number of left days.')
    response = driver.execute_script(script)
    response = json.loads(response["response"])
    logger.info("The result is: %d." % int(float(response["data"]["leftDays"])))


def glados(cookie, logger):
    driver = undetected_chromedriver.Chrome()
    driver.get("https://glados.rocks")

    driver.delete_all_cookies()
    for piece in cookie.split('; '):
        name = piece[:piece.find('=')]
        value = piece[piece.find('=') + 1:]
        if name in ["koa:sess", "koa:sess.sig"]:
            driver.add_cookie({"name": name, "value": value})

    if glados_checkin(driver, logger) != -2:
        glados_status(driver, logger)

    driver.close()
    driver.quit()


def pushplus(token, log_path, logger):
    with open(log_path, 'r') as log_file:
        content = log_file.read()

    data = {'channel': 'wechat', "token": token,
            'title': 'Auto-GLaDOS Log File', "content": content}

    logger.info('')
    logger.info("Start to send message.")
    send_post = requests.post("https://www.pushplus.plus/send", data = data)
    send_json = send_post.json()

    if send_json['code'] == 200:
        logger.info('Successfully send message.')
    else:
        logger.info('Fail to send Message')


if __name__ == "__main__":
    os.environ["TZ"] = "Asia/Shanghai"
    time.tzset()

    log_dir = "logs/"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(level = logging.INFO)
    log_path = "logs/%s.log" % time.strftime("%Y%m%d%H%M", time.localtime())
    log_handler = logging.FileHandler(log_path, mode = "w")
    log_formatter = logging.Formatter("%(asctime)s: %(message)s")
    log_handler.setFormatter(log_formatter)
    logger = logging.getLogger(__name__)
    logger.addHandler(log_handler)

    cookie, token = get_account(logger = logger)

    glados(cookie, logger)
    pushplus(token, log_path, logger)
