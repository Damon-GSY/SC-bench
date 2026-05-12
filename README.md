## SupChain-Bench

A comprehensive benchmark for evaluating LLM tool-use and multi-step reasoning capabilities in supply chain order management scenarios.

### Overview

SupChain-Bench simulates a realistic three-tier supply chain system (Trade → Fulfillment → Warehouse) where models must navigate complex hierarchical relationships to answer natural language queries. Models are evaluated on their ability to make strategic function calls, chain multiple tool invocations with conditional logic, and produce accurate structured answers.

**Key Features**:
- **Realistic Supply Chain Simulation**: Three-tier order management with authentic business logic including cancellations, errors, and status tracking
- **Tool-Grounded Evaluation**: Models must make strategic function calls to retrieve information from a simulated database
- **Multi-Step Reasoning**: Questions demand chaining multiple tool calls with conditional logic based on intermediate results

### Project Structure

```
.
├── README.md
├── config/
│   ├── prompt_tool_sessions.yaml           # Standard system/user prompts
│   ├── prompt_react_reasoning.yaml         # ReAct-style prompts
│   ├── prompt_tool_sessions_with_sop.yaml  # SOP-guided prompts
│   └── prompts/
│       ├── generate_question_prompt.md     # Question generation prompt template
│       ├── generate_answer_prompt.md       # Answer generation prompt template
│       └── prompt_tool_sessions_with_sop.md
├── data/
│   ├── TradeOrders.csv                     # Trade order data
│   ├── FulfillmentOrders.csv               # Fulfillment order data
│   ├── WarehouseOrders.csv                 # Warehouse order data
│   ├── ErrorLogs.csv                       # Error logs
│   ├── CancellationContext.csv             # Cancellation metadata
│   ├── tool_use_question.jsonl             # Tool-use benchmark questions
│   ├── tool_use_answers.jsonl              # Tool-use benchmark ground-truth answers
│   ├── multiple_choices_clean.jsonl        # Multiple-choice questions
│   ├── single_choices_clean.jsonl          # Single-choice questions
│   └── true_false_clean.jsonl              # True/false questions
├── src/
│   └── tool.py                             # Tool definitions, schemas, and registry
├── scripts/
│   └── evaluation.py                       # Evaluation script
├── generate_data.py                        # Synthetic dataset generation
└── get_results.py                          # Deterministic result orchestration (ground truth)
```

### Data Schema

The benchmark uses five CSV tables representing a hierarchical order management system:

| Table | Key Fields | Description |
|-------|-----------|-------------|
| **TradeOrders** | `trade_order_id`, `buyer_id` | Top-level customer orders |
| **FulfillmentOrders** | `fulfillment_order_id`, `trade_order_id`, `biz_status` | Fulfillment units within trade orders |
| **WarehouseOrders** | `warehouse_order_id`, `fulfillment_order_id`, `status`, `error_code` | Warehouse-level execution units |
| **ErrorLogs** | `entity_type`, `warehouse_order_id`, `fulfillment_order_id`, `code`, `text` | Detailed error information |
| **CancellationContext** | `entity_type`, `entity_id`, `cancel_type`, `reason_code`, `reason_text` | Cancellation metadata |

Each trade order contains 1–5 fulfillment orders, and each fulfillment contains 1–3 warehouse orders.

### Tool API

The benchmark provides **8 function tools** (defined in `src/tool.py`) that models can call:

| # | Tool | Purpose | Key Output |
|---|------|---------|------------|
| 1 | `query_buyer_and_related` | Entry point: get buyer info + related order IDs | `buyer_id`, `related_item[]` |
| 2 | `get_fulfillment_status` | Get aggregated fulfillment status | `status` |
| 3 | `get_cancel_scenes` | Get cancellation initiator | `cancelType` (BUYER/SELLER) |
| 4 | `get_cancel_error_code` | Get cancellation reason | `cancelErrorCode`, `cancelErrorMsg` |
| 5 | `get_error_reason` | Get fulfillment-level error details | `code`, `text` |
| 6 | `check_fake_shipping` | Check for fake shipping flags | `exceptionFlag` |
| 7 | `get_warehouse_status` | Get warehouse order status | `status`, `error` |
| 8 | `get_warehouse_error_details` | Get detailed warehouse error info | `code`, `text` |

**Conditional Tool-Calling Flow**:
```
query_buyer_and_related(order_id)
  └─ for each fulfillment_id:
       get_fulfillment_status(fulfillment_id)
         ├─ if "cancelled" → get_cancel_scenes → get_cancel_error_code
         │                    (optional: check_fake_shipping)
         ├─ if "error"     → get_error_reason
         └─ for each warehouse_order_id:
              get_warehouse_status → get_warehouse_error_details
```

The OpenAI-compatible function tool schemas are exported as the `tools` list and `TOOL_REGISTRY` dict in `src/tool.py`, ready to be plugged into any LLM API client.

### Setup

**Prerequisites**: Python 3.8+

**Install dependencies**:
```bash
pip install pandas numpy
```

### Usage

#### 1. Generate Synthetic Data

```bash
python generate_data.py
```

Configurable parameters: `num_trades` (default: 100), `cancel_rate` (0.15), `error_rate` (0.10), `seed` (42).

#### 2. Generate Ground Truth

`get_results.py` deterministically orchestrates tool calls for a given question and produces the expected structured answer:

```bash
python get_results.py "What is the status of order T1030?"
```

#### 3. Integrate with Your Inference Pipeline

Import the tool definitions and registry into your own inference code:

```python
from src.tool import tools, TOOL_REGISTRY

# `tools` — OpenAI-compatible function schemas, pass to your API call
# `TOOL_REGISTRY` — name → callable mapping, use to execute tool calls locally
```

Prompt templates are available in `config/` for different strategies (standard, ReAct, SOP-guided).

#### 4. Evaluate Results

```bash
python scripts/evaluation.py \
  -g data/tool_use_answers.jsonl \
  -p your_model_predictions.jsonl \
  -o results/evaluation/eval.json
```

Optional flags:
- `-q` / `--questions`: Path to questions JSONL to include question text in mismatch reports
- `--details-limit`: Limit number of mismatches in stdout preview (default: 50)

### Evaluation Metrics

**Entity-Level Precision/Recall**:
- **Trade Order Level**: `trade_order_id`, `buyer_id`
- **Fulfillment Order Level**: `fulfillment_id`, `status`, `cancel_type`, `reason_code`, `reason_text`, `errorCode`, `errorText`
- **Warehouse Order Level**: `warehouse_order_id`, `status`, `errorCode`, `errorText`

**Conditional Logic Evaluation** covers three flows:
1. **Normal Flow**: Status tracking without errors/cancellations
2. **Cancellation Flow**: Requires `cancel_type`, `reason_code`, `reason_text`
3. **Error Flow**: Requires `errorCode` and `errorText`

### Prediction Format

Each line in the predictions JSONL file must contain a `tool_trace` array. The evaluator parses this trace to reconstruct the structured answer and compare it against ground truth.

```json
{
  "tool_trace": [
    {
      "step": 1,
      "name": "query_buyer_and_related",
      "arguments": {"order_id": "T1030"},
      "output": {
        "buyer_id": {"id": 90029},
        "related_item": [
          {"fulfillment_id": "FO2080", "warehouse_order_id": "WO3170"}
        ]
      }
    },
    {
      "step": 2,
      "name": "get_fulfillment_status",
      "arguments": {"fulfillment_id": "FO2080"},
      "output": {"status": "packing_in_progress"}
    },
    {
      "step": 3,
      "name": "get_warehouse_status",
      "arguments": {"fulfillment_id": "FO2080", "warehouse_order_id": "WO3170"},
      "output": {"status": "packing_in_progress", "error": null}
    }
  ]
}
```

Each `tool_trace` entry must have:
- **`name`**: One of the 8 tool names (e.g. `query_buyer_and_related`)
- **`arguments`**: The arguments passed to the tool (dict)
- **`output`**: The tool's return value (dict)

The evaluator automatically reconstructs trade/fulfillment/warehouse structures from the trace and compares field-by-field against ground truth.

### License

Copyright (c) 2025 AIDC-SupplyChain-AI

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this project except in compliance with the License.
You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the [LICENSE](./LICENSE) file for the specific language governing
permissions and limitations under the License.

Third-party software notices and additional attributions can be found in
[THIRD-PARTY-NOTICES](./THIRD-PARTY-NOTICES).
