#coding:utf-8
import os
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright, name) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.sysucc.org.cn/linchuangzhuanjia")  # 此时的page.content()就是网页源代码了
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name=name).click()
    page1 = page1_info.value
    # page1.locator("#block-sysu-cc-content div").filter(has_text="徐瑞华 职务：中山大学肿瘤防治中心主任、医院院长、研究所所长，华南恶性肿瘤防治全国重点实验室主任 职称：教授，博士生导师、结直肠癌内科首席专家 专长 消化道肿瘤").nth(1).click()
    text = page1.inner_text('#block-sysu-cc-content div')
    with open(f"data/{name}.txt","w",encoding="utf-8") as f:
        f.write(text)
    print(text)
    page1.close()
    page.close()

    # ---------------------
    context.close()
    browser.close()

names = ['陈明', '陈东', '孙鹏']

#重名没管
names = list(set(names))

errs=[]
errinfo = []
for name in names:
    try:
        if os.path.isfile(f"{name}.txt"):
            continue
        with sync_playwright() as playwright:
            run(playwright,name=name)
    except Exception as e:
        errs.append(name)
        errinfo.append(str(e))
        print(name)
        print(e)
print(errs)
