import requests
import time
from utils.db_check import DatabricksSPClient
from dotenv import load_dotenv
import os
import json

load_dotenv()
def query_databricks(workspace_url: str, access_token: str, warehouse_id: str, sql: str):
    """
    Databricks SQL Warehouse API를 통해 SQL 실행 후 결과를 반환하는 함수

    Args:
        workspace_url (str): Databricks 워크스페이스 URL (예: https://<workspace>.databricks.com)
        access_token (str): Personal Access Token
        warehouse_id (str): 사용할 SQL Warehouse ID
        sql (str): 실행할 SQL 쿼리

    Returns:
        dict: 쿼리 결과 JSON
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 1. 쿼리 실행 요청
    submit_url = f"{workspace_url}/api/2.0/sql/statements"
    payload = {
        "statement": sql,
        "warehouse_id": warehouse_id,
        "wait_timeout": "30s",  # 결과 기다리는 시간
        "on_wait_timeout": "CONTINUE"  # 바로 안 끝나면 나중에 polling
    }

    response = requests.post(submit_url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    statement_id = data["statement_id"]

    # 2. 실행 상태 확인 (polling)
    status_url = f"{workspace_url}/api/2.0/sql/statements/{statement_id}"
    while True:
        res = requests.get(status_url, headers=headers)
        res.raise_for_status()
        state_data = res.json()

        state = state_data.get("status", {}).get("state")
        if state in ("SUCCEEDED", "FAILED", "CANCELED"):
            break
        time.sleep(2)

    if state != "SUCCEEDED":
        raise Exception(f"Query failed with state: {state}")

    return state_data.get("result", {})

    # result = state_data.get("result", {})
    #
    # # 컬럼명 추출, 없으면 기본 이름 생성
    # rows = result.get("data_array", [])
    # columns_info = result.get("columns", [])
    # if columns_info:
    #     columns = [col.get("name", f"col{i}") for i, col in enumerate(columns_info)]
    # else:
    #     # 컬럼 정보가 없으면 0,1,2,...로 기본 생성
    #     columns = [f"col{i}" for i in range(len(rows[0]))] if rows else []
    #
    # # 컬럼 전체 표시
    # pd.set_option("display.max_columns", None)
    #
    # # 행 전체 표시 (많으면 주의)
    # pd.set_option("display.max_rows", None)
    #
    # # 열 값 전체 길이 표시
    # pd.set_option("display.max_colwidth", None)
    # df = pd.DataFrame(rows, columns=columns)
    # return df


workspace_url = "https://adb-3951005985438017.17.azuredatabricks.net"
access_token = os.getenv('secret_key')
warehouse_id = "d42f11fa1dd58612"
with open("json/test_srp.json", "r", encoding="utf-8") as f:
    data = json.load(f)
product_ids_case1 = []

for case_group in data:  # 리스트 안의 dict 순회
    case1_items = case_group.get("case2", {})  # case1만 가져오기
    for _, info in case1_items.items():
        product_id = info.get("상품번호")
        if product_id:
            product_ids_case1.append(product_id)

print(product_ids_case1)
print(','.join(map(str, product_ids_case1)))
print(','.join(f"'{x}'" for x in product_ids_case1))

sql = f"""
    SELECT item_no, ins_date
    FROM baikali1xs.ad_ats_silver.ub_ra_click_gmkt
    WHERE ins_date >= '2025-10-17 11:36:41'
      AND cguid = '11758850530814005372000000'
      AND item_no IN ({','.join(f"'{x}'" for x in product_ids_case1)})
      AND dt = '20251017'
      AND hour IN ('11', '12');
    """

sql2 = """
    SELECT item_no, dt, hour
    FROM baikali1xs.ad_ats_silver.ub_ad_cpc_click_gmkt
    WHERE item_no IN ('2588353016','4399796464')
      AND cguid = '11758850530814005372000000';
    """
result = query_databricks(workspace_url, access_token, warehouse_id, sql)
db_check = DatabricksSPClient()

click_time = "2025-10-15 10:15:21"
goodscode = "3522530029"
print(result)
print(type(result))
db_check.assert_db_record_time(result, click_time, goodscode)