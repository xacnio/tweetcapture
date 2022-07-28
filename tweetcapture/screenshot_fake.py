import re
from selenium.webdriver.common.by import By

class TweetCaptureFake:
    image_url = "https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png"
    
    fake = False
    name = ""
    username = ""
    content = ""
    image = ""
    verified = None

    def create(self, name="", content="", username=None, image="", verified=None):
        username = username.replace("\"", "\\\"") if username is not None else None
        image = image.replace("\"", "\\\"") if image is not None else None
        content = content.replace("\"", "\\\"") if content is not None else None
        name = name.replace("\"", "\\\"")

        if len(image) > 0:
            if image == "default":
                self.image = self.image_url
            else:
                self.image = self.image_url if (image is None or len(image) == 0) else (image if image.startswith("http") else image_base64(image))
        self.name = name
        self.username = "" if username is None or len(username) == 0 else (username if username.startswith('@') else '@' + username)
        if content is not None:
            self.content = self.content_style(content)
        if verified is not None:
            self.verified = True if verified is True else False
        
        if self.verified is not None or (self.name is not None and len(self.name) > 0) or (self.username is not None and len(self.username) > 0) or \
            (self.content is not None and len(self.content) > 0) or (self.image is not None and len(self.image) > 0):
            self.fake = True

    def content_style(self, content):
        COLOR = "#1b95e0"
        twitter_hashtag_re = re.compile(r'#(\w+)')
        twitter_usertag_re = re.compile(r'@(\w+)')
        twitter_url_re = re.compile(r"""(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))?""")
        content = twitter_hashtag_re.sub(lambda m: '<span style="color: %s;display:inline;">%s</span>' % (COLOR, m.group(0)), content)
        content = twitter_usertag_re.sub(lambda m: '<span style="color: %s;display:inline;">%s</span>' % (COLOR, m.group(0)), content)
        content = twitter_url_re.sub(lambda m: '<span style="color: %s;display:inline;">%s</span>' % (COLOR, m.group(0)), content)
        return content

    def process(self, color, base, driver):
        if self.fake is False:
            return

        VERIFIED_XPATH = base + "/article/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/a/div/div[1]/div[2]"
        if self.verified is not None:
            try:
                if self.verified is False: 
                    xpath_vrf = driver.find_element(By.XPATH, VERIFIED_XPATH)
                    execute_script(f"""arguments[0].innerHTML = "";""", xpath_vrf)
                else:
                    THEME_1 = """r-13gxpu9"""
                    THEME_2 = """r-jwli3a"""
                    THEME_3 = """r-1fmj7o5"""
                    xpath_vrf = driver.find_element(By.XPATH, VERIFIED_XPATH)
                    VERIFIED_CONTENT = f"""<svg viewBox="0 0 24 24" class="{THEME_1 if color == 0 else (THEME_2 if color == 1 else THEME_3)} r-4qtqp9 r-yyyyoo r-1xvli5t r-dnmrzs r-bnwqim r-1plcrui r-lrvibr" style="margin-left: 2px;"><g><path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484zm-6.616-3.334l-4.334 6.5c-.145.217-.382.334-.625.334-.143 0-.288-.04-.416-.126l-.115-.094-2.415-2.415c-.293-.293-.293-.768 0-1.06s.768-.294 1.06 0l1.77 1.767 3.825-5.74c.23-.345.696-.436 1.04-.207.346.23.44.696.21 1.04z"></path></g></svg>"""
                    driver.execute_script(f"""arguments[0].innerHTML = '{VERIFIED_CONTENT}';""", xpath_vrf)
            except:
                pass
        
        if self.name is not None and len(self.name) > 0:
            try:
                NAME_XPATH = base + "/article/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/a/div/div/div/span/span"
                driver.execute_script(f"""arguments[0].innerHTML = "{self.name}";""", driver.find_element(By.XPATH, NAME_XPATH))
            except:
                pass
        if self.username is not None and len(self.username) > 0:
            try:
                USERNAME_XPATH = base + "/article/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/a/div/div[2]/div/span"
                driver.execute_script(f"""arguments[0].innerHTML = "{self.username}";""", driver.find_element(By.XPATH, USERNAME_XPATH))
            except:
                pass
        try:
            if self.content is not None and len(self.content) > 0:
                content = driver.find_element(By.XPATH, base + "/article/div/div/div/div[3]") or None
                driver.execute_script("""
                if(arguments[0].childNodes[0].innerHTML.search('lang="') != -1) {
                    arguments[0].childNodes[0].childNodes[0].childNodes[0].innerHTML = arguments[1]
                } else {
                    arguments[0].childNodes[1].childNodes[0].childNodes[0].innerHTML = arguments[1]
                }
                """, content, self.content)
        except:
            pass

        if self.image is not None and len(self.image) > 0:
            IMG_XPATH = base + "/article/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/a/div[3]/div/div/div/div"
            IMG2_XPATH = base + "/article/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/a/div[3]/div/div/div/img"
            backgroundImage = self.image
            try:
                driver.execute_script("""
                    var image = new Image();
                    var img = arguments[0];
                    image.onload = function () {
                        img.style.backgroundImage = 'url("""+backgroundImage+""")';
                    };
                    image.onerror = function () {
                        img.style.backgroundImage = 'url("""+self.image_url+""")';
                    };
                    image.src = '"""+backgroundImage+"""';
                """, driver.find_element(By.XPATH, IMG_XPATH), driver.find_element(By.XPATH, IMG2_XPATH))
            except:
                pass