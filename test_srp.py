import time

from pom.SrpPage import Srp
from pom.Etc import Etc
from utils.db_check import DatabricksSPClient
import json
from utils.TimeLogger import TimeLogger
import pytest
from case_data.search_data import search_testcases1, search_testcases2, search_testcases3, search_testcases4
import io
import contextlib
from datetime import datetime, timedelta


@pytest.fixture(scope="module")
def file_start_time():
    # 이 모듈(파일) 내 테스트가 처음 실행될 때 한 번만 호출됨
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
@pytest.fixture(scope="module")
def file_start_dt():
    # 이 모듈(파일) 내 테스트가 처음 실행될 때 한 번만 호출됨
    return datetime.now().strftime("%Y%m%d")
#--
@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("keyword, case_id", search_testcases1, ids=[c for _, c in search_testcases1])
def test_srp_1(page, keyword, case_id, request):
    # TestRail 케이스 ID를 현재 실행 노드에 저장
    request.node._testrail_case_id = case_id
    etc = Etc(page)
    srp_page = Srp(page)
    logger = TimeLogger("json/test_srp.json")

    output_content = io.StringIO()
    with contextlib.redirect_stdout(output_content):

        # g마켓 홈 으로 이동
        etc.goto()
        # 일반회원 로그인
        etc.login("t4adbuy01", "Gmkt1004!!")
        # keyword 로 검색창에 검색
        srp_page.search_product(keyword)
        # 상품 노출 확인시간 저장
        logger.record_time("case1", keyword,"exposure")
        # 먼저 둘러보세요 모듈로 이동 후 확인
        srp_page.search_module_by_title("먼저 둘러보세요")
        # 먼저 둘러보세요 모듈내 광고 상품 곽인
        goodscode = srp_page.assert_item_in_module("먼저 둘러보세요")
        # 상품 번호 저장
        logger.record_goodscode("case1",keyword, goodscode)
        # 상품 클릭시간 저장
        logger.record_time("case1", keyword,"click")
        # 상품 클릭후 해당 vip 이동 확인
        srp_page.montelena_goods_click(goodscode)
    # hook에서 사용하기 위해 item에 저장
    request.node._stdout_capture = output_content.getvalue()

@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("keyword, case_id", search_testcases2, ids=[c for _, c in search_testcases2])
def test_srp_2(page, keyword, case_id, request):
    # TestRail 케이스 ID를 현재 실행 노드에 저장
    request.node._testrail_case_id = case_id
    etc = Etc(page)
    srp_page = Srp(page)
    logger = TimeLogger("json/test_srp.json")


    output_content = io.StringIO()
    with contextlib.redirect_stdout(output_content):
        # g마켓 홈 으로 이동
        etc.goto()
        # 일반회원 로그인
        etc.login("t4adbuy01", "Gmkt1004!!")
        # keyword 로 검색창에 검색
        srp_page.search_product(keyword)
        # 상품 노출 확인시간 저장
        logger.record_time("case2", keyword,"exposure")
        # 일반상품 모듈로 이동 후 확인
        parent = srp_page.search_module_by_title("일반상품")
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
    # hook에서 사용하기 위해 item에 저장
    request.node._stdout_capture = output_content.getvalue()

# def test_wait_15min():
#     time.sleep(930)
click_db = None
imp_db = None
vimp_db = None

def test_fetch_from_db(file_start_time, file_start_dt):
    db_check = DatabricksSPClient()  # Databricks 클라이언트 객체 생성

    # 전역 변수로 조회 결과를 저장 (다른 테스트에서 재사용)
    global click_db, imp_db, vimp_db

    with open("json/test_srp.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 상품번호만 뽑기
    product_ids = []
    for case_group in data:
        for case, items in case_group.items():
            for _, info in items.items():
                product_ids.append(info["상품번호"])

    # 1. 클릭 로그(click_db) 조회
    sql = f"""
    SELECT item_no, ins_date
    FROM baikali1xs.ad_ats_silver.ub_ad_cpc_click_gmkt
    WHERE ins_date >= '{file_start_time}'
      AND cguid = '11758850530814005372000000'
      AND dt = '{file_start_dt}';
    """
    click_db = db_check.query_databricks(sql)
    time.sleep(10)  # 조회 후 10초 대기 (DB 처리 반영 시간 고려)

    # 2. 노출 로그(imp_db) 조회
    sql = f"""
    SELECT item_no, ins_date
    FROM baikali1xs.ad_ats_silver.ub_ad_cpc_imp_gmkt
    WHERE ins_date >= '{file_start_time}'
      AND cguid = '11758850530814005372000000'
      AND item_no IN ({','.join(map(str, product_ids))})
      AND dt = '{file_start_dt}';
    """
    imp_db = db_check.query_databricks(sql)
    time.sleep(10)  # 조회 후 10초 대기

    # 3. 가상노출 로그(vimp_db) 조회
    sql = f"""
    SELECT item_no, ins_date
    FROM baikali1xs.ad_ats_silver.ub_ad_cpc_vimp_gmkt
    WHERE ins_date >= '{file_start_time}'
      AND cguid = '11758850530814005372000000'
      AND item_no IN ({','.join(map(str, product_ids))})
      AND dt = '{file_start_dt}';
    """
    vimp_db = db_check.query_databricks(sql)

@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("keyword, case_id", search_testcases3,ids=[c for _, c in search_testcases3])
def test_srp_3(keyword, case_id, request):
    # TestRail 케이스 ID를 현재 실행 노드에 저장
    request.node._testrail_case_id = case_id
    db_check = DatabricksSPClient()
    with open("json/test_srp.json", "r", encoding="utf-8") as f:
        test_record = json.load(f)

    output_content = io.StringIO()
    with contextlib.redirect_stdout(output_content):
        # JSON에서 테스트에 필요한 값 추출
        goodscode = test_record[0]["case1"][keyword]["상품번호"]   # 상품 번호
        click_time = test_record[0]["case1"][keyword]["click"]     # 클릭 발생 시간
        expose_time = test_record[0]["case1"][keyword]["exposure"] # 노출 발생 시간

        # DB 기록 검증
        # - click_db : 클릭 로그 DB, 클릭 시간 검증
        # - imp_db   : 노출 로그 DB, 노출 시간 검증
        # - vimp_db  : 가상 노출 로그 DB, 노출 시간 검증
        db_check.assert_db_record_time(click_db, click_time, goodscode)
        db_check.assert_db_record_time(imp_db, expose_time, goodscode)
        db_check.assert_db_record_time(vimp_db, expose_time, goodscode)

    # hook에서 사용하기 위해 item에 저장
    request.node._stdout_capture = output_content.getvalue()

@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.parametrize("keyword, case_id", search_testcases4, ids=[c for _, c in search_testcases3])
def test_srp_4(keyword, case_id, request):
    # TestRail 케이스 ID를 현재 실행 노드에 저장
    request.node._testrail_case_id = case_id
    db_check = DatabricksSPClient()
    with open("json/test_srp.json", "r", encoding="utf-8") as f:
        test_record = json.load(f)
    output_content = io.StringIO()
    with contextlib.redirect_stdout(output_content):
        # JSON에서 테스트에 필요한 값 추출
        goodscode = test_record[0]["case2"][keyword]["상품번호"]  # 상품 번호
        click_time = test_record[0]["case2"][keyword]["click"]  # 클릭 발생 시간
        expose_time = test_record[0]["case2"][keyword]["exposure"]  # 노출 발생 시간

        # DB 기록 검증
        # - click_db : 클릭 로그 DB, 클릭 시간 검증
        # - imp_db   : 노출 로그 DB, 노출 시간 검증
        # - vimp_db  : 가상 노출 로그 DB, 노출 시간 검증
        db_check.assert_db_record_time(click_db, click_time, goodscode)
        db_check.assert_db_record_time(imp_db, expose_time, goodscode)
        db_check.assert_db_record_time(vimp_db, expose_time, goodscode)

    # hook에서 사용하기 위해 item에 저장
    request.node._stdout_capture = output_content.getvalue()
