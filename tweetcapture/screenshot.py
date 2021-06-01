from asyncio import sleep, run
from tweetcapture.utils.webdriver import get_driver
from tweetcapture.utils.utils import is_valid_tweet_url, get_tweet_file_name, get_tweet_base_url, get_chromedriver_default_path, image_base64
from os.path import abspath
from tweetcapture.screenshot_fake import TweetCaptureFake
import base64

class TweetCapture:
    driver = None
    driver_path = None
    mode = 0
    night_mode = 0
    chrome_opts = []
    lang = None
    Fake = None

    def __init__(self, mode=0, night_mode=0):
        self.set_night_mode(night_mode)
        self.set_mode(mode)
        self.driver_path = get_chromedriver_default_path()
        self.Fake = TweetCaptureFake()

    async def screenshot(self, url, path=None, mode=None, night_mode=None):
        if self.Fake.fake is True:
            url = "https://twitter.com/jack/status/20" if len(url) == 0 or not url.startswith("http") else url
            if not isinstance(path, str) or len(path) == 0:
                path = "tweet_image_fake.png"
        else: 
            if is_valid_tweet_url(url) is False:
                raise Exception("Invalid tweet url")

            if not isinstance(path, str) or len(path) == 0:
                path = get_tweet_file_name(url)

        url = is_valid_tweet_url(url)
        if self.lang:
            url += "?lang=" + self.lang

        driver = await get_driver(self.chrome_opts, self.driver_path)
        driver.get(url)
        driver.add_cookie(
            {"name": "night_mode", "value": str(night_mode or self.night_mode)})
        driver.get(url)
        await sleep(3.0)
        base = f"//a[translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='{get_tweet_base_url(url)}']/ancestor::article/.."
        content = driver.find_element_by_xpath(base)
        self.Fake.process(night_mode or self.night_mode, base, driver)
        self.__margin_tweet(mode or self.mode, driver, base)
        driver.execute_script(self.__code_footer_items(mode or self.mode), driver.find_element_by_xpath(base + "/article/div/div/div/div[3]") or driver.find_element_by_xpath(base + "/article/div/div/div/div[2]"), driver.find_element_by_xpath(base + "/article/div/div/div/div[2]/div[2]/div/div/div[1]/div[2]"))
        self.__hide_items(mode or self.mode, driver, base)
        await sleep(2.0)
        content.screenshot(path)
        driver.close()
        return path
        

    def get_night_mode(self):
        return self.night_mode

    def set_night_mode(self, night_mode):
        if 0 <= night_mode <= 2:
            self.night_mode = night_mode

    def set_mode(self, mode):
        self.mode = mode

    def add_chrome_argument(self, option):
        self.chrome_opts.append(option)

    def set_lang(self, lang):
        self.lang = lang

    def set_chromedriver_path(self, path):
        self.driver_path = path

    def __hide_items(self, mode, driver, base):
        finded = []
        HIDE_ITEMS_XPATH = ['/html/body/div/div/div/div[1]','/html/body/div/div/div/div[2]/header', '/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[1]']
        for item in HIDE_ITEMS_XPATH:
            try:
                element = driver.find_element_by_xpath(item)
                driver.execute_script("""
                arguments[0].style.display="none";
                """, element)
            except:
                continue

    def __margin_tweet(self, mode, driver, base):
        if mode == 0 or mode == 1:
            try:
                driver.execute_script(
                    """arguments[0].parentNode.style.marginBottom = '35px';""", driver.find_element_by_xpath(base+"/article/div"))
            except:
                pass

    def __code_footer_items(self, mode):
        if mode == 3:
            return """arguments[1].style.display="none";"""
        
        if mode == 2:
            keys = [2]
        elif mode == 1:
            keys = [0,2]
        else:
            keys = [0,1,2]
        return """
        var items = [""" + ",".join(str(v) for v in keys) + """];
        var length = arguments[0].childNodes.length;
        arguments[1].style.display="none";
        if(arguments[0].childNodes[length-2].innerHTML.search("/retweets") == -1 && arguments[0].childNodes[length-2].innerHTML.search("/likes") == -1) {
            if(items.length == 3) items = [0,1]
            else if(items.length == 2) items = [0,1]
            else items = [1]
            for(var i = length-2, x = 0; i < length; i++, x++) {
                if(items.includes(x))
                    arguments[0].childNodes[i].style.display="none";
            }
        }
        else {
            for(var i = length-3, x = 0; i < length; i++, x++) {
                if(items.includes(x))
                    arguments[0].childNodes[i].style.display="none";
                if(items.includes(0) && x == 1)
                    arguments[0].childNodes[i].style.marginTop = '15px';
            }
        }
        """