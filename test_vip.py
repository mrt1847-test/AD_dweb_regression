import time

from pom.VipPage import Vip
from pom.Etc import Etc
from utils.TimeLogger import TimeLogger
from utils.db_check import DatabricksSPClient
import pytest
from case_data.vip_data import vip_testcases1, vip_testcases2, vip_testcases3, vip_testcases4
import json
import io
import contextlib

#pipenv run pytest --cache-clear test.py

@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("goods_num, case_id", vip_testcases1, ids=[c for _, c in vip_testcases1])
def test_vip_1(page, goods_num, case_id, request):
    request.node._testrail_case_id = case_id
    etc = Etc(page)
    vip_page = Vip(page)
    logger = TimeLogger("json/test_vip.json")

    output_content = io.StringIO()
    with contextlib.redirect_stdout(output_content):

        etc.goto()
        # 일반회원 로그인
        etc.login("t4adbuy01", "Gmkt1004!!")

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
    # hook에서 사용하기 위해 item에 저장
    request.node._stdout_capture = output_content.getvalue()

@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("goods_num, case_id", vip_testcases2, ids=[c for _, c in vip_testcases2])
def test_vip_2(page, goods_num, case_id, request):
    request.node._testrail_case_id = case_id
    logger = TimeLogger("json/test_vip.json")
    etc = Etc(page)
    vip_page = Vip(page)
    output_content = io.StringIO()
    with contextlib.redirect_stdout(output_content):

        etc.goto()
        # 일반회원 로그인
        etc.login("t4adbuy01", "Gmkt1004!!")

        # vip 로 이동
        etc.goto_vip(goods_num)

        # BT 모듈로 이동 후 확인
        logger.record_time("case2", goods_num, "exposure")
        parent = vip_page.vip_module_by_title("함께 구매하면 좋은 상품이에요")
        # 광고 태그 확인
        result = vip_page.check_bt_ad_tag(parent)
        goodscode = result["goodscode"]
        logger.record_goodscode("case2", goods_num, goodscode)
        target = result["target"]
        # 상품 클릭후 해당 vip 이동 확인
        logger.record_time("case2", goods_num, "click")
        vip_page.click_goods(goodscode, target)

    # hook에서 사용하기 위해 item에 저장
    request.node._stdout_capture = output_content.getvalue()
#

# def test_wait_15min():
#     time.sleep(930)
#
@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("goods_num, case_id", vip_testcases3, ids=[c for _, c in vip_testcases3])
def test_srp_3(goods_num, case_id, request):
    # TestRail 케이스 ID를 현재 실행 노드에 저장
    request.node._testrail_case_id = case_id
    db_check = DatabricksSPClient()
    with open("json/test_vip.json", "r", encoding="utf-8") as f:
        test_record = json.load(f)
    output_content = io.StringIO()
    with contextlib.redirect_stdout(output_content):
        goodscode = test_record[0]["case1"][goods_num]["상품번호"]
        click_time = test_record[0]["case1"][goods_num]["click"]
        # sql = f"select ins_date, cguid from baikali1xs.ad_ats_silver.ub_ad_cpc_click_gmkt where ins_date >='{click_time}' and item_no ='{goodscode}' and cguid = '11412244806446005562000000' limit 10 ;"
        # a= db_check.query_databricks(sql)
        # print(a)
    # hook에서 사용하기 위해 item에 저장
    request.node._stdout_capture = output_content.getvalue()


@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("goods_num, case_id", vip_testcases4, ids=[c for _, c in vip_testcases4])
def test_srp_4(goods_num, case_id, request):
    # TestRail 케이스 ID를 현재 실행 노드에 저장
    request.node._testrail_case_id = case_id
    db_check = DatabricksSPClient()
    with open("json/test_vip.json", "r", encoding="utf-8") as f:
        test_record = json.load(f)
    output_content = io.StringIO()
    with contextlib.redirect_stdout(output_content):
        goodscode = test_record[0]["case2"][goods_num]["상품번호"]
        click_time = test_record[0]["case2"][goods_num]["click"]
        # sql = f"select ins_date, cguid from baikali1xs.ad_ats_silver.ub_ad_cpc_click_gmkt where ins_date >='{click_time}' and item_no ='{goodscode}' and cguid = '11412244806446005562000000' limit 10 ;"
        # a= db_check.query_databricks(sql)
        # print(a)
    # hook에서 사용하기 위해 item에 저장
    request.node._stdout_capture = output_content.getvalue()