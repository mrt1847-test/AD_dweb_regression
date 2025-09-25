from playwright.sync_api import Page, expect


class Srp():
    def __init__(self, page):
        self.page = page

    def search_product(self, keyword: str):
        """
        홈화면에서 특정 keyword로 검색
        :param (str) keyword : 검색어
        :example:
        """
        runtext = f'Home > {keyword}검색'
        print("#", runtext, "시작")
        self.page.fill("input[name='keyword']", keyword)
        self.page.press("input[name='keyword']", "Enter")
        print("#", runtext, "종료")

    def search_module_by_title(self, module_title):
        """
        특정 모듈의 타이틀 텍스트를 통해 해당 모듈 노출 확인하고 그 모듈 엘리먼트를 반환
        :param (str) module_title : 모듈 타이틀
        :return: 해당 모듈 element
        :example:
        """
        runtext = f'SRP > {module_title}모듈 노출 확인'
        print("#", runtext, "시작")
        child = self.page.get_by_text(module_title)
        child.scroll_into_view_if_needed()
        parent = child.locator("xpath=../..")
        expect(parent).to_be_visible()
        print("#", runtext, "종료")

        return parent


    def assert_item_in_module(self, module_title):

        """
        특정 모듈의 타이틀 텍스트를 통해 해당 모듈내 상품 노출 확인하고 그상품번호 반환
        :param (str) module_title : 모듈 타이틀
        :return: 해당 모듈 노출 상품 번호
        :example:
        """
        runtext = f'SRP > {module_title}모듈내 상품 노출 확인'
        print("#", runtext, "시작")
        child = self.page.get_by_text("먼저 둘러보세요")
        parent = child.locator("xpath=../..")
        target = parent.locator("div.box__item-container > div.box__image > a")
        target.scroll_into_view_if_needed()
        expect(target).to_be_visible()
        goodscode = target.get_attribute("data-montelena-goodscode")
        print("#", runtext, "종료")
        
        return goodscode

    def montelena_goods_click(self, goodscode):
        """
        특정 상품 번호 아이템 클릭
        :param (str) goodscode : 상품 번호
        :return (str) url: 클릭한 상품 url
        :example:
        """
        runtext = f'SRP > {goodscode} 상품 클릭'
        print("#", runtext, "시작")

        element = self.page.locator(f'a[data-montelena-goodscode="{goodscode}"]').nth(0)

        # 새 페이지 대기
        with self.page.context.expect_page() as new_page_info:
            element.click()
        new_page = new_page_info.value

        url = new_page.url
        assert goodscode in url, f"상품 번호 {goodscode}가 URL에 포함되어야 합니다"
        print("#", runtext, "종료")

        runtext = f'SRP > {goodscode} 상품 이동확인'
        print("#", runtext, "시작")
        assert goodscode in url, f"상품 번호 {goodscode}가 URL에 포함되어야 합니다"
        print("#", runtext, "종료")

        return url

