As a professional supply chain understanding expert, your task is to generate all the information needed to answer the question based on the requirements.
You are provided with all the relevant information needed to answer this question. Please read and understand this information carefully, and then generate a json object as a reference answer.
Your generated answer must be a json object, and the content inside it must come from the provided relevant information,
1. **You must not include any content unrelated to the relevant information**
2. **The generate field must exactly match the field showed in relevant information, you should not make up any information**
3. **The generated answer should be used as a reference for constructing the final answer**

# Question
{question}

# Relevant Information
{context_info}

# Example
For example, if the question is "For fulfillment order F02060, What is the warehouse_order_status of it", and the relevant information is
<relevant_info>
{"trade_order_id": "T2002", "buyer_id": {
  "id": 90019
}, "fulfillments": [{"fulfillment_order_id": "FO2058", "trade_order_id": "T2002", "biz_status": "in_transit", "warehouse_orders": [{"warehouse_order_id": "WO3116", "fulfillment_order_id": "FO2058", "status": "in_transit", "error_code": 1}, {"warehouse_order_id": "WO3117", "fulfillment_order_id": "FO2058", "status": "in_transit", "error_code": 1}, {"warehouse_order_id": "WO3118", "fulfillment_order_id": "FO2058", "status": "packing_done", "error_code": 1}]}, {"fulfillment_order_id": "FO2059", "trade_order_id": "T2002", "biz_status": "packing_in_progress", "warehouse_orders": [{"warehouse_order_id": "WO3119", "fulfillment_order_id": "FO2059", "status": "packing_in_progress", "error_code": 1}, {"warehouse_order_id": "WO3120", "fulfillment_order_id": "FO2059", "status": "packing_done", "error_code": 1}]}, {"fulfillment_order_id": "FO2060", "trade_order_id": "T2002", "biz_status": "in_transit", "warehouse_orders": [{"warehouse_order_id": "WO3121", "fulfillment_order_id": "FO2060", "status": "in_transit", "error_code": 1}, {"warehouse_order_id": "WO3122", "fulfillment_order_id": "FO2060", "status": "packing_done", "error_code": 1}, {"warehouse_order_id": "WO3123", "fulfillment_order_id": "FO2060", "status": "packing_done", "error_code": 1}]}]}
</relevant_info>
Because question is asking for the warehouse_order_status of fulfillment order F02060, you don't need other fulfillments information, so you should generate the following json object as the reference answer:
<generated_answer>
{"trade_order_id":"T2002","buyer_id":{"id":90019},"fulfillments":[{"fulfillment_order_id":"FO2060","trade_order_id":"T2002","biz_status":"in_transit","warehouse_orders":[{"warehouse_order_id":"WO3121","fulfillment_order_id":"FO2060","status":"in_transit","error_code":1},{"warehouse_order_id":"WO3122","fulfillment_order_id":"FO2060","status":"packing_done","error_code":1},{"warehouse_order_id":"WO3123","fulfillment_order_id":"FO2060","status":"packing_done","error_code":1}]}]}
</generated_answer>