import requests
import time
from dotenv import load_dotenv
import os
load_dotenv()

class DatabricksSPClient:
    def __init__(self):

        self.workspace_url = "https://adb-3951005985438017.17.azuredatabricks.net"
        self.warehouse_id = "d42f11fa1dd58612"
        self.access_token = os.getenv("secret_key")

    def query_databricks(self, sql: str, wait_timeout="30s"):
        """Databricks SQL Warehouse에서 쿼리 실행 후 DataFrame으로 반환"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # 1. 쿼리 실행 요청
        submit_url = f"{self.workspace_url}/api/2.0/sql/statements"
        payload = {
            "statement": sql,
            "warehouse_id": self.warehouse_id,
            "wait_timeout": wait_timeout,
            "on_wait_timeout": "CONTINUE"
        }
        res = requests.post(submit_url, headers=headers, json=payload)
        res.raise_for_status()
        statement_id = res.json()["statement_id"]

        # 2. 쿼리 실행 상태 확인 (polling)
        status_url = f"{self.workspace_url}/api/2.0/sql/statements/{statement_id}"
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

        # 3. 결과를 DataFrame으로 변환
        result = state_data.get("result", {})
        return result