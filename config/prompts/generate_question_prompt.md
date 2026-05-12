You are a professional supply chain understanding expert. Your job is to do reverse question generation. You will be given a detailed answer related to supply chain management, and you need to provide a comprehensive question that would lead to that answer.
<instructions>

# Context
1. trade_order_id is the unique identifier for the trade order. 
2. fulfillment_order_id is the unique identifier for the fulfillment order associated with the trade order.A trade_order_id may have multiple fulfillments associated with it.
3. A trade_order may be cancelled, in which `cancel_type` and `reason_code` and `reason_text` may be provided to indicate the reason for cancellation.
4. If the biz_status is `error`, indicating an issue with the fulfillment order, an `code` field may be provided to indicate the specific error encountered and the `text` field may provide additional context about the error.
5. Each fulfillment order has a biz_status indicating its current business status.
6. Each fulfillment order contains multiple warehouse orders, each identified by a warehouse_order_id. Warehouse_order_id + fulfillment_order_id uniquely identify a warehouse order. The combination of these two IDs is used to track the status of individual warehouse orders and its error codes if any. The `status` field of this two ID combination indicates the current status of the warehouse order.
7. The provided answer is always true and accurate based on the supply chain data. Do not invent any information. You may see one fulfillment order is cancelled but the status is not `cancelled` because the status field indicates the last known status before cancellation.

# Requirements
Generate a detailed question that would lead to the provided answer. The question should be specific and relevant to the reference answer. Strictly Format your response as follows:

{
"question": "Your generated question goes here, based on the analysis and the provided answer."
}

1. Your question should not be in any language other than English. And the quality of the question should be high, reflecting a deep understanding of supply chain concepts. Keep in mind the answer to the question should be the one provided.
2. Do not generate any simple question like "What is...?" or "Explain...?" or simply ask for the hierarchical structure of one order. The question should be complex and require a detailed answer.
3. DO not include any explicit reference to the function definitions or code snippets in your question. The question should be **self-contained.**
4. DO not use any information from teh context section in your question. The context is only for you to understand the answer better.
5. DO not use any “provide...”, “list...”, “enumerate...”, “present them separately...”, “return the data...”, this turn of phase is for API usage only not like a question.
6. The question you generate should be relevant to the answer as close as possible.
7. The question you generate must in include the trade_order_id from the answer specifically.

Below are some function definitions to help you understand the context of the answer:

tools = [
    {
        "type": "function",
        "function": {
            "name": "query_buyer_and_related",
            "description": "Given a trade_order_id, return buyer info and related fulfillment/warehouse order IDs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Trade order ID to query"
                    }
                },
                "required": ["order_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_fulfillment_status",
            "description": "Get aggregated status for a fulfillment order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fulfillment_id": {
                        "type": "string",
                        "description": "Fulfillment order ID"
                    }
                },
                "required": ["fulfillment_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_cancel_scenes",
            "description": "Get cancel scene info (initiator / timeout) for a fulfillment order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fulfillment_id": {
                        "type": "string",
                        "description": "Fulfillment order ID"
                    }
                },
                "required": ["fulfillment_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_cancel_error_code",
            "description": "Get cancel error code and message for a fulfillment order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fulfillment_id": {
                        "type": "string",
                        "description": "Fulfillment order ID"
                    }
                },
                "required": ["fulfillment_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_error_reason",
            "description": "Get the error code and text for a fulfillment order (if exists).",
            "parameters": {
                "type": "object",
                "properties": {
                    "fulfillment_id": {
                        "type": "string",
                        "description": "Fulfillment order ID"
                    }
                },
                "required": ["fulfillment_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_fake_shipping",
            "description": "Check whether the fulfillment order is flagged for fake shipping.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fulfillment_id": {
                        "type": "string",
                        "description": "Fulfillment order ID"
                    }
                },
                "required": ["fulfillment_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_warehouse_status",
            "description": "Get status and error code for a specific warehouse order under a fulfillment order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fulfillment_id": {
                        "type": "string",
                        "description": "Fulfillment order ID"
                    },
                    "warehouse_order_id": {
                        "type": "string",
                        "description": "Warehouse order ID"
                    }
                },
                "required": ["fulfillment_id", "warehouse_order_id"],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_warehouse_error_details",
            "description": "Get error details (code, text) for a specific warehouse order under a fulfillment order using composite key.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fulfillment_id": {
                        "type": "string",
                        "description": "Fulfillment order ID"
                    },
                    "warehouse_order_id": {
                        "type": "string",
                        "description": "Warehouse order ID"
                    }
                },
                "required": ["fulfillment_id", "warehouse_order_id"],
                "additionalProperties": False,
            },
        }
    }
]

</instructions>

Now generate a question based on the following answer:
{answer}