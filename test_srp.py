
from pom.SrpPage import Srp
from pom.Etc import Etc
from utils.db_check import DatabricksSPClient
import json
from utils.TimeLogger import TimeLogger
import pytest
from case_data.search_data import search_testcases1, search_testcases2, search_testcases3, search_testcases4


#--
@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("keyword, case_id", search_testcases1, ids=[c for _, c in search_testcases1])
def test_srp_1(page, keyword, case_id, request):
    # TestRail 케이스 ID를 현재 실행 노드에 저장
    request.node._testrail_case_id = case_id
    etc = Etc(page)
    srp_page = Srp(page)
    logger = TimeLogger("json/test_srp.json")

    # g마켓 홈 으로 이동
    etc.goto()
    # 일반회원 로그인
    etc.login("t4adbuy01", "Gmkt1004!!")
    # keyword 로 검색창에 검색
    srp_page.search_product(keyword)
    # 먼저 둘러보세요 모듈로 이동 후 확인
    srp_page.search_module_by_title("먼저 둘러보세요")
    # 상품 노출 확인시간 저장
    logger.record_time("case1", keyword,"exposure")
    # 먼저 둘러보세요 모듈내 광고 상품 곽인
    goodscode = srp_page.assert_item_in_module("먼저 둘러보세요")
    # 상품 번호 저장
    logger.record_goodscode("case1",keyword, goodscode)
    # 상품 클릭시간 저장
    logger.record_time("case1", keyword,"click")
    # 상품 클릭후 해당 vip 이동 확인
    srp_page.montelena_goods_click(goodscode)

@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("keyword, case_id", search_testcases2, ids=[c for _, c in search_testcases2])
def test_srp_2(page, keyword, case_id, request):
    # TestRail 케이스 ID를 현재 실행 노드에 저장
    request.node._testrail_case_id = case_id
    etc = Etc(page)
    srp_page = Srp(page)
    logger = TimeLogger("json/test_srp.json")

    # g마켓 홈 으로 이동
    etc.goto()
    # 일반회원 로그인
    etc.login("t4adbuy01", "Gmkt1004!!")
    # keyword 로 검색창에 검색
    srp_page.search_product(keyword)
    # 일반상품 모듈로 이동 후 확인
    parent = srp_page.search_module_by_title("일반상품")
    # 상품 노출 확인시간 저장
    logger.record_time("case2", keyword,"exposure")
    # 일반상품 모듈내 광고 상품 비율 곽인
    srp_page.hybrid_ratio_check(parent)
    # 광고상품 상품 번호 추출
    goodscode = srp_page.assert_ad_item_in_hybrid(parent)
    # 상품 번호 저장
    logger.record_goodscode("case2",keyword, goodscode)
    # 상품 클릭시간 저장
    logger.record_time("case2", keyword,"click")
    # 상품 클릭후 해당 vip 이동 확인
    srp_page.montelena_goods_click(goodscode)

# def test_wait_15min():
#     time.sleep(930)
#
@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("keyword, case_id", search_testcases3, ids=[c for _, c in search_testcases3])
def test_srp_3(keyword, case_id, request):
    # TestRail 케이스 ID를 현재 실행 노드에 저장
    request.node._testrail_case_id = case_id
    db_check = DatabricksSPClient()
    with open("json/test_srp.json", "r", encoding="utf-8") as f:
        test_record = json.load(f)
    goodscode = test_record[0]["case1"][keyword]["상품번호"]
    click_time = test_record[0]["case1"][keyword]["click"]
    # sql = f"select ins_date, cguid from baikali1xs.ad_ats_silver.ub_ad_cpc_click_gmkt where ins_date >='{click_time}' and item_no ='{goodscode}' and cguid = '11412244806446005562000000' limit 10 ;"
    # a= db_check.query_databricks(sql)
    # print(a)

@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("keyword, case_id", search_testcases4, ids=[c for _, c in search_testcases3])
def test_srp_4(keyword, case_id, request):
    # TestRail 케이스 ID를 현재 실행 노드에 저장
    request.node._testrail_case_id = case_id
    db_check = DatabricksSPClient()
    with open("json/test_srp.json", "r", encoding="utf-8") as f:
        test_record = json.load(f)
    goodscode = test_record[0]["case2"][keyword]["상품번호"]
    click_time = test_record[0]["case2"][keyword]["click"]
    # sql = f"select ins_date, cguid from baikali1xs.ad_ats_silver.ub_ad_cpc_click_gmkt where ins_date >='{click_time}' and item_no ='{goodscode}' and cguid = '11412244806446005562000000' limit 10 ;"
    # a= db_check.query_databricks(sql)
    # print(a)
