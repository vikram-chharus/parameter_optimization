def set_input(stock,  indicator, data):
    return {
    "name": "Testing",
    "time_frame": "ONE_HOUR",
    "symbol": stock,
    "entry_action": "buy",
    "qty": 100,
    "entry_condn": [{
    "left": [
        {
        "value_position": 0,
        "type": "TI",
        "name": indicator, 
        "attributes": {
            "column": "close", 
            "period": data["window"] if "window" in data.keys() else 14
        }
        }
    ],
    "compare": "crosses below",
    "right": [
        {
        "type": "number",
        "value": data["entry"] if "entry" in data.keys() else 30

        }
    ]
    }],
    "exit_condn": [{
    "left": [
        {
        "value_position": 0,
        "type": "TI",
        "name": indicator, 
        "attributes": {
            "column": "close", 
            "period": data["window"] if "window" in data.keys() else 14
        }
        }
    ],
    "compare": "crosses over",
    "right": [
        {
        "type": "number",
        "value": data["exit"] if "exit" in data.keys() else 70
        }
    ]
    }],
    "tgt_prcnt": 10,
    "sl_prcnt": 10,
    "start_datetime": 1516386600.0,
    "end_datetime": 1616178600.0  
    }
    
