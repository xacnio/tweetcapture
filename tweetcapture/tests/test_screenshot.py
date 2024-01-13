import cv2
from tweetcapture import TweetCapture
from asyncio import run
import unittest
from os import remove, environ
from os.path import exists
import glob
import numpy as np

class TestScreenshot(unittest.TestCase):
    tweetcapture = None
    url = ""
    output_path = ""
    result_path = ""

    def __init__(self, *args, **kwargs):
        self.tweetcapture = TweetCapture(test=True, overwrite=True)
        self.tweetcapture.set_lang('en')
        super(TestScreenshot, self).__init__(*args, **kwargs)

        if environ.get('AUTH_TOKEN') != None:
            self.tweetcapture.set_cookies([{'name': 'auth_token', 'value': environ.get('AUTH_TOKEN')}])

        # Delete all test files
        files = glob.glob('*.png')
        for f in files:
            remove(f)

    def begin(self, tweet_url, output_path, result_path):
        self.url = tweet_url
        self.output_path = output_path
        self.result_path = result_path
        if exists(output_path): remove(output_path)       
        if exists(result_path): remove(result_path)

    # Main screenshot test
    def test_screenshot1(self):
        self.begin("https://twitter.com/jack/status/20", "test1.png", "result1.png")

        print(f"Screenshot test1 started: {self.url} -> {self.output_path}")

        filename = run(self.tweetcapture.screenshot(self.url, self.output_path, mode=3, night_mode=2))
        
        self.assertEqual(filename, self.output_path, "File name not equal with output filename")
        self.assertTrue(exists(filename), "File not exists")
        
        print(f"Checking similarity with test images...")

        image= cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)        

        for i in range(1,3):
            template = cv2.imread(f"../assets/test/1/crop{i}.png", 0)
            try:
                result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            except cv2.error as err:
                raise err
        
            m = result.max()
            print(f"Image {i} checked: %%%.2g" % m)
            min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)

            height, width= template.shape[:2]

            top_left= max_loc
            bottom_right= (top_left[0] + width, top_left[1] + height)
            cv2.rectangle(image, top_left, bottom_right, (0,0,255),5)
            
            assert (m > 0.85), "Screenshot is not matching with template"

        cv2.imwrite(self.result_path, image)

    # Mode tests
    def test_screenshot2(self):
        self.begin("https://twitter.com/jack/status/20", "test2.png", "result2.jpg")

        print(f"Screenshot test2 started.")

        ITEMS = ['../assets/test/2/button.png', '../assets/test/2/info.png', '../assets/test/2/time.png']
        MODES = [
            [False, False, False], # Hide everything outside tweet content and author
            [False, True, False], # Show retweet/like counts
            [False, True, True], # Show retweet/like counts and timestamp
            [True, True, True], # Show everything
            [False, False, True], # Show timestamp
        ]
        
        for mode, _ in enumerate(MODES):
            self.output_path = f"test2_mode{mode}.png"
            self.result_path = f"result2_mode{mode}.png"
            if exists(self.output_path): remove(self.output_path)
            filename = run(self.tweetcapture.screenshot(self.url, self.output_path, mode=mode))
            self.assertEqual(filename, self.output_path, "File name not equal with output filename")
            self.assertTrue(exists(filename), "File not exists")

            print(f"Mode {mode}: Checking similarity with test images...")
            image= cv2.imread(filename)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   

            for j, item in enumerate(ITEMS):
                template = cv2.imread(item, 0)
                try:
                    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
                except cv2.error as err:
                    raise err
            
                m = result.max()
                
                is_exist = (m > 0.80)
                if is_exist:
                    min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)
                    height, width= template.shape[:2]
                    top_left= max_loc
                    bottom_right= (top_left[0] + width, top_left[1] + height)
                    cv2.rectangle(image, top_left, bottom_right, (0,0,255),5)
                print(f"Mode {mode}: Item: {j} Check: %%%.2g Expect: {MODES[mode][j]} Result: {is_exist}" % m)
                assert (is_exist == MODES[mode][j]), f"Screenshot mode {mode} is not matching with template"

            cv2.imwrite(self.result_path, image)

    # Hide photos test
    def test_screenshot_hidephotos(self):
        self.begin("https://twitter.com/elonmusk/status/1527418023069503511", "testhidephoto.png", "resulthidephoto.png")

        print(f"Screenshot hide photos test started.")

        self.tweetcapture.hide_media(photos=True)
        filename = run(self.tweetcapture.screenshot(self.url, self.output_path, mode=3))
        self.assertEqual(filename, self.output_path, "File name not equal with output filename")
        self.assertTrue(exists(filename), "File not exists")

        print(f"Checking similarity with test images...")

        image= cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)        

        template = cv2.imread(f"../assets/test/hidephotos/image.png", 0)
        try:
            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        except cv2.error as err:
            raise err
    
        m = result.max()
        expect = False
        is_exist = (m > 0.80)
        if is_exist:
            min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)
            height, width= template.shape[:2]
            top_left= max_loc
            bottom_right= (top_left[0] + width, top_left[1] + height)
            cv2.rectangle(image, top_left, bottom_right, (0,0,255),5)
            cv2.imwrite(self.result_path, image)
        
        print(f"Screenshot checked: %%%.2g Expect: {expect} Result: {is_exist}" % m)
        assert (is_exist == expect), f"Screenshot has a photo, it is not matching with template"

    # Hide gifs test
    def test_screenshot_hidegifs(self):
        self.begin("https://twitter.com/elonmusk/status/1521195604596113408", "testhidegif.png", "resulthidegif.png")

        print(f"Screenshot hide gifs test started.")

        self.tweetcapture.hide_media(gifs=True)
        filename = run(self.tweetcapture.screenshot(self.url, self.output_path, mode=3))
        self.assertEqual(filename, self.output_path, "File name not equal with output filename")
        self.assertTrue(exists(filename), "File not exists")

        print(f"Checking similarity with test images...")

        image= cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)        

        template = cv2.imread(f"../assets/test/hidegifs/image.png", 0)
        try:
            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        except cv2.error as err:
            raise err
    
        m = result.max()
        expect = False
        is_exist = (m > 0.80)
        if is_exist:
            min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)
            height, width= template.shape[:2]
            top_left= max_loc
            bottom_right= (top_left[0] + width, top_left[1] + height)
            cv2.rectangle(image, top_left, bottom_right, (0,0,255),5)
            cv2.imwrite(self.result_path, image)
        
        print(f"Screenshot checked: %%%.2g Expect: {expect} Result: {is_exist}" % m)
        assert (is_exist == expect), f"Screenshot has a gif, it is not matching with template"

    # Hide videos test
    def test_screenshot_hidevideos(self):
        self.begin("https://twitter.com/elonmusk/status/1533408313894912001", "testhidevideo.png", "resulthidevideo.png")

        print(f"Screenshot hide videos test started.")

        self.tweetcapture.hide_media(videos=True)
        filename = run(self.tweetcapture.screenshot(self.url, self.output_path, mode=3))
        self.assertEqual(filename, self.output_path, "File name not equal with output filename")
        self.assertTrue(exists(filename), "File not exists")

        print(f"Checking screenshot height...")

        image= cv2.imread(filename)
        h, _, _ = image.shape
        assert (h < 400), f"Screenshot has a video"

    # Hide quotes test
    def test_screenshot_hidequotes(self):
        self.begin("https://twitter.com/X/status/1722695941348569464", "testhidequote.png", "resulthidequote.png")

        print(f"Screenshot hide quotes test started.")

        self.tweetcapture.hide_media(quotes=True)
        filename = run(self.tweetcapture.screenshot(self.url, self.output_path, mode=3))
        self.assertEqual(filename, self.output_path, "File name not equal with output filename")
        self.assertTrue(exists(filename), "File not exists")

        print(f"Checking similarity with test images...")

        image= cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)        

        template = cv2.imread(f"../assets/test/hidequotes/image.png", 0)
        try:
            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        except cv2.error as err:
            raise err
    
        m = result.max()
        expect = False
        is_exist = (m > 0.80)
        if is_exist:
            min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)
            height, width= template.shape[:2]
            top_left= max_loc
            bottom_right= (top_left[0] + width, top_left[1] + height)
            cv2.rectangle(image, top_left, bottom_right, (0,0,255),5)
            cv2.imwrite(self.result_path, image)
        
        print(f"Screenshot checked: %%%.2g Expect: {expect} Result: {is_exist}" % m)
        assert (is_exist == expect), f"Screenshot has a quote, it is not matching with template"

    # Show parent tweet test
    @unittest.skip("The test disabled because guests cannot see parent tweets")
    def test_screenshot_showparent(self):
        self.begin("https://twitter.com/elonmusk/status/940125978797281281", "testshowparent.png", "resultshowparent.png")

        print(f"Screenshot show parent tweet test started.")

        filename = run(self.tweetcapture.screenshot(self.url, self.output_path, mode=3, show_parent_tweets=True))
        self.assertEqual(filename, self.output_path, "File name not equal with output filename")
        self.assertTrue(exists(filename), "File not exists")

        print(f"Checking similarity with test images...")

        image= cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)        

        template = cv2.imread(f"../assets/test/sp/image.png", 0)
        try:
            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        except cv2.error as err:
            raise err
    
        m = result.max()
        expect = True
        is_exist = (m > 0.80)
        if is_exist:
            min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)
            height, width= template.shape[:2]
            top_left= max_loc
            bottom_right= (top_left[0] + width, top_left[1] + height)
            cv2.rectangle(image, top_left, bottom_right, (0,0,255),5)
            cv2.imwrite(self.result_path, image)
        
        print(f"Screenshot checked: %%%.2g Expect: {expect} Result: {is_exist}" % m)
        assert (is_exist == expect), f"Screenshot has not a parent tweet, it is not matching with template"

    # Show mentions test
    @unittest.skip("The test disabled because guests cannot see mentions")
    def test_screenshot_showmentions(self):
        self.begin("https://twitter.com/superwhatevr/status/1040704190748798976", "testshowmentions.png", "resultshowmentions.png")

        print(f"Screenshot show mentions test started.")

        filename = run(self.tweetcapture.screenshot(self.url, self.output_path, mode=3, show_mentions_count=10))
        self.assertEqual(filename, self.output_path, "File name not equal with output filename")
        self.assertTrue(exists(filename), "File not exists")

        print(f"Checking similarity with test images...")

        image= cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)        

        template = cv2.imread(f"../assets/test/sm/image.png", 0)
        try:
            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        except cv2.error as err:
            raise err

        height, width= template.shape[:2]
        (y_points, x_points) = np.where(result > 0.95)
        boxes = []
        for (x, y) in zip(x_points, y_points):
            boxes.append((x, y, x + width, y + height))

        for (x1, y1, x2, y2) in boxes:
            cv2.rectangle(image, (x1, y1), (x2, y2), (0,0,255),5)
        
        cv2.imwrite(self.result_path, image)

        expect_count = 2
        count = len(boxes)
        
        print(f"Screenshot checked. Expect: {expect_count} Result: {count}")
        assert (count == expect_count), f"Screenshot has not a mention, it is not matching with template"


if __name__ == '__main__':
    unittest.main(warnings='ignore')