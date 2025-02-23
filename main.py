import time
from playwright.sync_api import Playwright, sync_playwright

# 댓글 삭제
def deleteCmnt(page, cmntList):
    for cmnt in cmntList:
        print("https://www.teamblind.com" + cmnt)
        page.goto("https://www.teamblind.com" + cmnt)
        while True:
            try:
                # 댓글 펼치기
                count = 0
                while True:
                    try:
                        page.query_selector("button.btn-reply").click()
                        count = 0
                    except:
                        count += 1
                        if count > 3: break
                        else: page.wait_for_timeout(500)
                
                # 삭제
                page.get_by_text("삭제", exact=True).locator("../../../../../..").first.wait_for(timeout=500)
                page.get_by_text("삭제", exact=True).locator("../../../../../..").first.click()
                page.get_by_text("삭제", exact=True).first.click()
                page.get_by_role("button", name="삭제").click()
            except:
                print("댓글 삭제 완료\n")
                break

# 항목 분류
def postsCategory(page, posts_list):
    # item = ["post", "cmnt", "poll"]

    # for i in item:
    #     print("{}: {}".format(i, len([element.get_attribute("href") for element in posts_list.query_selector_all("li." + i + " div.tit a")])))

    deleteCmnt(page, set([element.get_attribute("href") for element in posts_list.query_selector_all("li.cmnt div.tit a")]))

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.teamblind.com/kr/")

    # 로그인
    page.get_by_role("button", name="로그인").click()
    otp = page.query_selector("div.otp-code strong").inner_text()
    print("OTP Code: {}".format(otp))

    # 작성한 글 페이지 이동
    page.get_by_role("button", name="내 메뉴").wait_for(timeout=60000)
    page.get_by_role("button", name="내 메뉴").click()
    page.get_by_role("link", name="내가 작성한 글").click()

    print("작성한 글을 확인하고 있습니다...")

    # 작성한 글 전체 확인
    pageHeight = page.evaluate("document.body.scrollHeight")
    latestTime = time.time()

    while time.time() - latestTime < 5:
        page.keyboard.press("PageDown")
        page.wait_for_timeout(100)

        newPageHeight = page.evaluate("document.body.scrollHeight")

        if newPageHeight > pageHeight:
            pageHeight = newPageHeight
            latestTime = time.time()

    # 항목 분류
    postsCategory(page, page.query_selector("div.posts_list"))

    # 스크립트 종료
    context.close()
    browser.close()

with sync_playwright() as playwright:
    print("블라인드 정리 스크립트")
    print("웹 로그인이 필요하니 앱을 준비하세요.")
    print("blind App > 마이페이지 > 블라인드 웹 로그인 > 인증번호 입력")
    run(playwright)
