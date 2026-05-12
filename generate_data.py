import json
import os
import random
from typing import Any, Dict, List

import numpy as np
import pandas as pd

BASE_DIR = "./data"
os.makedirs(BASE_DIR, exist_ok=True)


def write_fixed_samples():
    # Trade orders
    trade = pd.DataFrame([
        {"trade_order_id": "T1001", "buyer_id": json.dumps(
            {"id": 90001}, ensure_ascii=False)},
        {"trade_order_id": "T1002", "buyer_id": json.dumps(
            {"id": 90002}, ensure_ascii=False)},
        {"trade_order_id": "T1003", "buyer_id": json.dumps(
            {"id": 90003}, ensure_ascii=False)},
        {"trade_order_id": "T1004", "buyer_id": json.dumps(
            {"id": 90004}, ensure_ascii=False)},
        {"trade_order_id": "T1005", "buyer_id": json.dumps(
            {"id": 90005}, ensure_ascii=False)}
    ])

    # Fulfillment orders
    fo = pd.DataFrame([
        {"fulfillment_order_id": "FO2001",
            "trade_order_id": "T1001", "biz_status": "PROCESSING"},
        {"fulfillment_order_id": "FO2002",
            "trade_order_id": "T1002", "biz_status": "SHIPPED"},
        {"fulfillment_order_id": "FO2003",
            "trade_order_id": "T1003", "biz_status": "CANCELLED"},
        {"fulfillment_order_id": "FO2004",
            "trade_order_id": "T1004", "biz_status": "PROCESSING"},
        {"fulfillment_order_id": "FO2005",
            "trade_order_id": "T1005", "biz_status": "DELIVERED"}
    ])

    wo = pd.DataFrame([
        {"warehouse_order_id": "WO3001", "fulfillment_order_id": "FO2001",
            "status": "PACKING", "error_code": None},
        {"warehouse_order_id": "WO3002", "fulfillment_order_id": "FO2001",
            "status": "SHIPPED", "error_code": None},
        {"warehouse_order_id": "WO3003", "fulfillment_order_id": "FO2002",
            "status": "PACKED", "error_code": None},
        {"warehouse_order_id": "WO3004", "fulfillment_order_id": "FO2002",
            "status": "DELIVERED", "error_code": None},
        {"warehouse_order_id": "WO3005", "fulfillment_order_id": "FO2003",
            "status": "ERROR", "error_code": "PICK_SHORTAGE"},
        {"warehouse_order_id": "WO3006", "fulfillment_order_id": "FO2004",
            "status": "IN_TRANSIT", "error_code": None},
        {"warehouse_order_id": "WO3007", "fulfillment_order_id": "FO2005",
            "status": "DELIVERED", "error_code": None}
    ])

    # Error logs
    err = pd.DataFrame([
        {"entity_type": "warehouse_order", "warehouse_order_id": "WO3005",
            "fulfillment_order_id": "FO2003", "code": "PICK_SHORTAGE", "text": "Out of stock"},
        {"entity_type": "warehouse_order", "warehouse_order_id": "WO3005",
            "fulfillment_order_id": "FO2003", "code": "PACK_MISSING_LABEL", "text": "Missing shipping label"}
    ])

    # Cancellation context
    cancel = pd.DataFrame([
        {"entity_type": "fulfillment_order", "entity_id": "FO2003", "cancel_type": "BUYER",
            "reason_code": "BUYER_REQUEST", "reason_text": "buyer cancel"},
        {"entity_type": "fulfillment_order", "entity_id": "FO2004", "cancel_type": "SELLER",
            "reason_code": "TIMEOUT", "reason_text": "overtime cancel"}
    ])

    # Write CSV files
    trade.to_csv(os.path.join(BASE_DIR, "TradeOrders.csv"), index=False)
    fo.to_csv(os.path.join(BASE_DIR, "FulfillmentOrders.csv"), index=False)
    wo.to_csv(os.path.join(BASE_DIR, "WarehouseOrders.csv"), index=False)
    err.to_csv(os.path.join(BASE_DIR, "ErrorLogs.csv"), index=False)
    cancel.to_csv(os.path.join(
        BASE_DIR, "CancellationContext.csv"), index=False)

    print("Fixed samples written to ./data")


def generate_synthetic_data(num_trades=5,
                            cancel_rate=0.15,
                            error_rate=0.10,
                            seed=42):
    """
    Generate synthetic dataset for trade, fulfillment, warehouse, cancellation and error logs.

    Description:
    - Quantities per trade/fulfillment are randomly generated:
      * Fulfillment orders per trade: 1–5
      * Warehouse orders per fulfillment: 1–3
    - ErrorLogs table structure uses composite ID: (entity_type, warehouse_order_id, fulfillment_order_id, code, text).
    - Uses given seed to ensure reproducibility.
    """
    rng = random.Random(seed)
    np.random.seed(seed)

    # Fulfillment order biz_status constants
    FO_STATUS_NORMAL = ["PROCESSING", "SHIPPED", "DELIVERED"]
    FO_STATUS_CANCELLED = "CANCELLED"
    FO_STATUS_ERROR = "ERROR"

    # Cancellation and error handling constants
    CANCEL_TYPES = ["BUYER", "SELLER"]
    FO_ERROR_CODES = ["FAKE_SHIP", "WAREHOUSE_ISSUE"]
    FO_ERROR_TEXTS = ["fake shippment", "warehouse issue"]

    # Warehouse order status pool
    status_pool = ["PACKING", "PACKED", "SHIPPED", "IN_TRANSIT", "DELIVERED"]

    trade_rows: List[Dict[str, Any]] = []
    fo_rows: List[Dict[str, Any]] = []
    wo_rows: List[Dict[str, Any]] = []
    err_rows: List[Dict[str, Any]] = []
    cancel_rows: List[Dict[str, Any]] = []

    # ID counters
    trade_idx = 1001
    fo_idx = 2001
    wo_idx = 3001
    buyer_base = 90000

    for _ in range(num_trades):
        trade_id = f"T{trade_idx}"
        trade_idx += 1
        buyer_id_obj = {"id": buyer_base}
        buyer_base += 1
        trade_rows.append({"trade_order_id": trade_id, "buyer_id": json.dumps(
            buyer_id_obj, ensure_ascii=False)})

        for _ in range(rng.randint(1, 5)):
            fo_id = f"FO{fo_idx}"
            fo_idx += 1
            # Step 2: Randomly assign biz_status based on cancel_rate and error_rate
            rand_val = rng.random()
            if rand_val < cancel_rate:
                biz_status = FO_STATUS_CANCELLED
                is_cancelled = True
                is_error = False
            elif rand_val < cancel_rate + error_rate:
                biz_status = FO_STATUS_ERROR
                is_cancelled = False
                is_error = True
            else:
                biz_status = rng.choice(FO_STATUS_NORMAL)
                is_cancelled = False
                is_error = False

            fo_rows.append({"fulfillment_order_id": fo_id,
                           "trade_order_id": trade_id, "biz_status": biz_status})

            # Step 3: For cancelled fulfillment orders, randomly assign BUYER or SELLER as cancellation party
            if is_cancelled:
                reason_code = rng.choice(
                    ["OUT_OF_STOCK", "BUYER_REQUEST", "ADDRESS_ISSUE", "TIMEOUT"])
                reason_text = reason_code.lower().replace("_", " ").capitalize()
                cancel_rows.append({
                    "entity_type": "fulfillment_order",
                    "entity_id": fo_id,
                    "cancel_type": rng.choice(CANCEL_TYPES),
                    "reason_code": reason_code,
                    "reason_text": reason_text
                })

            # Step 4: For error fulfillment orders, record FAKE_SHIP or WAREHOUSE_ISSUE at fulfillment_order level
            if is_error:
                error_code = rng.choice(FO_ERROR_CODES)
                error_text = FO_ERROR_TEXTS[FO_ERROR_CODES.index(error_code)]
                err_rows.append({
                    "entity_type": "fulfillment_order",
                    "warehouse_order_id": "",
                    "fulfillment_order_id": fo_id,
                    "code": error_code,
                    "text": error_text
                })

            for _ in range(rng.randint(1, 3)):
                wo_id = f"WO{wo_idx}"
                wo_idx += 1
                # Error vs normal (keep warehouse order error logic separate from fulfillment order error logic)
                if rng.random() < error_rate and not is_cancelled:
                    status = "ERROR"
                    error_code = rng.choice(
                        ["PICK_SHORTAGE", "PACK_MISSING_LABEL", "SHIP_LOST", "SCAN_FAIL"])
                    # Record log at warehouse level
                    err_rows.append({
                        "entity_type": "warehouse_order",
                        "warehouse_order_id": wo_id,
                        "fulfillment_order_id": fo_id,
                        "code": error_code,
                        "text": error_code.lower().replace("_", " ")
                    })
                else:
                    # Normal flow
                    status = rng.choice(status_pool)
                    error_code = None

                wo_rows.append({
                    "warehouse_order_id": wo_id,
                    "fulfillment_order_id": fo_id,
                    "status": status,
                    "error_code": error_code
                })

    # Build DataFrames
    trade_df = pd.DataFrame(trade_rows, columns=["trade_order_id", "buyer_id"])
    fo_df = pd.DataFrame(
        fo_rows, columns=["fulfillment_order_id", "trade_order_id", "biz_status"])
    wo_df = pd.DataFrame(wo_rows, columns=[
                         "warehouse_order_id", "fulfillment_order_id", "status", "error_code"])
    err_df = pd.DataFrame(err_rows, columns=[
                          "entity_type", "warehouse_order_id", "fulfillment_order_id", "code", "text"])
    cancel_df = pd.DataFrame(cancel_rows, columns=[
                             "entity_type", "entity_id", "cancel_type", "reason_code", "reason_text", "timeout_flag"])

    # Write CSV files
    trade_df.to_csv(os.path.join(BASE_DIR, "TradeOrders.csv"), index=False)
    fo_df.to_csv(os.path.join(BASE_DIR, "FulfillmentOrders.csv"), index=False)
    wo_df.to_csv(os.path.join(BASE_DIR, "WarehouseOrders.csv"), index=False)
    err_df.to_csv(os.path.join(BASE_DIR, "ErrorLogs.csv"), index=False)
    cancel_df.to_csv(os.path.join(
        BASE_DIR, "CancellationContext.csv"), index=False)
    print(f"Synthetic dataset written to {BASE_DIR}")
    print(f"Trades={len(trade_df)}, Fulfillments={len(fo_df)}, Warehouses={len(wo_df)}, Errors={len(err_df)}, Cancellations={len(cancel_df)}")


if __name__ == "__main__":
    generate_synthetic_data(
        num_trades=100,
        cancel_rate=0.15,  # Rate of FOs that will be CANCELLED
        error_rate=0.10,   # Rate of FOs that will be ERROR
        seed=42
    )
