from pom.VipPage import Vip
from pom.Etc import Etc
from utils.TimeLogger import TimeLogger
import pytest
from case_data.vip_data import vip_testcases1, vip_testcases2
#pipenv run pytest --cache-clear test.py

@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("goods_num, case_id", vip_testcases1, ids=[c for _, c in vip_testcases1])
def test_vip_1(page, goods_num, case_id, request):
    request.node._testrail_case_id = case_id
    etc = Etc(page)
    vip_page = Vip(page)
    logger = TimeLogger("json/test_vip.json")
    # vip 로 이동
    etc.goto_vip(goods_num)

    # VT 모듈로 이동 후 확인
    logger.record_time("case1", goods_num, "exposure")
    parent = vip_page.vip_module_by_title("함께 보면 좋은 상품이에요")
    # 광고상품 상품 번호 추출
    result = vip_page.assert_item_in_module("함께 보면 좋은 상품이에요")
    goodscode = result["goodscode"]
    logger.record_goodscode("case1",goods_num, goodscode)
    target = result["target"]
    # 상품 클릭후 해당 vip 이동 확인
    logger.record_time("case1", goods_num, "click")
    vip_page.click_goods(goodscode, target)

@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("goods_num, case_id", vip_testcases2, ids=[c for _, c in vip_testcases2])
def test_vip_2(page, goods_num, case_id, request):
    request.node._testrail_case_id = case_id
    logger = TimeLogger("json/test_vip.json")
    etc = Etc(page)
    vip_page = Vip(page)

    # vip 로 이동
    etc.goto_vip(goods_num)

    # BT 모듈로 이동 후 확인
    logger.record_time("case2", goods_num, "exposure")
    parent = vip_page.vip_module_by_title("함께 구매하면 좋은 상품이에요")
    # 광고 태그 확인
    result = vip_page.check_bt_ad_tag(parent)
    goodscode = result["goodscode"]
    logger.record_goodscode("case1", goods_num, goodscode)
    target = result["target"]
    # 상품 클릭후 해당 vip 이동 확인
    logger.record_time("case1", goods_num, "click")
    vip_page.click_goods(goodscode, target)