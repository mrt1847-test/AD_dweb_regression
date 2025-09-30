from pom.SrpPage import Srp
from pom.VipPage import Vip
from pom.Etc import Etc
from utils.db_check import DatabricksSPClient

#pipenv run pytest --cache-clear test.py

def test_vip_1(page):
    etc = Etc(page)
    vip_page = Vip(page)
    db_check = DatabricksSPClient()
    # vip 로 이동
    etc.goto_vip()

    # VT 모듈로 이동 후 확인
    parent = vip_page.vip_module_by_title("함께 보면 좋은 상품이에요")
    # 광고상품 상품 번호 추출
    result = vip_page.assert_item_in_module("함께 보면 좋은 상품이에요")
    goodscode = result["goodscode"]
    target = result["target"]
    # 상품 클릭후 해당 vip 이동 확인
    vip_page.click_goods(goodscode, target)


def test_vip_2(page):
    etc = Etc(page)
    vip_page = Vip(page)
    db_check = DatabricksSPClient()
    # vip 로 이동
    etc.goto_vip_starship()

    # BT 모듈로 이동 후 확인
    parent = vip_page.vip_module_by_title("함께 구매하면 좋은 상품이에요")
    # 광고 태그 확인
    result = vip_page.check_bt_ad_tag(parent)
    goodscode = result["goodscode"]
    target = result["target"]
    # 상품 클릭후 해당 vip 이동 확인
    vip_page.click_goods(goodscode, target)