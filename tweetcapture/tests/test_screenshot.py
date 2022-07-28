import cv2
from tweetcapture import TweetCapture
from asyncio import run
import unittest
from os import remove
from os.path import exists

class TestScreenshot(unittest.TestCase):
    def test_screenshot(self):
        url = "https://twitter.com/jack/status/20"
        output = "test.png"
        result_path = "result.jpg"

        if exists(output):
            remove(output)       

        if exists(result_path):
            remove(result_path)

        print(f"Screenshot test started: {url} -> {output}")

        tweet = TweetCapture(test=True)
        filename = run(tweet.screenshot("https://twitter.com/jack/status/20", output, mode=3, night_mode=2))
        
        self.assertEqual(filename, output, "File name not equal with output filename")
        self.assertTrue(exists(filename), "File not exists")
        
        print(f"Checking similarity with test images...")

        image= cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)        

        for i in range(1,5):
            template = cv2.imread(f"../assets/crop{i}.png", 0)

            try:
                result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            except cv2.error as err:
                raise err
        
            m = result.max()
            print(f"Image {i} checked: {m}%")
            min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)

            height, width= template.shape[:2]

            top_left= max_loc
            bottom_right= (top_left[0] + width, top_left[1] + height)
            cv2.rectangle(image, top_left, bottom_right, (0,0,255),5)
            
            assert (m > 0.85), "Screenshot is not matching with template"

        cv2.imwrite(result_path, image)

if __name__ == '__main__':
    unittest.main(warnings='ignore')