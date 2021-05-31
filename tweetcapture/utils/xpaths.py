HIDE_ITEMS_XPATH = ['//*[@id="layers"]/div[2]',
                    '/html/body/div/div/div/div[2]/header']


def footer_xpath(base, i):
    return base + f"""/article/div/div/div/div[3]/div[{i}]"""
