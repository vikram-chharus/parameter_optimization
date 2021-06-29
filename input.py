def set_input(stock,  indicator, value):
    return {
    "name": "Startegy name",
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
            "period": value
        }
        }
    ],
    "compare": "crosses below",
    "right": [
        {
        "type": "number",
        "value": 30
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
            "period": value
        }
        }
    ],
    "compare": "crosses over",
    "right": [
        {
        "type": "number",
        "value": 70
        }
    ]
    }],
    "tgt_prcnt": 10,
    "sl_prcnt": 10,
    "start_datetime": 1516386600.0,
    "end_datetime": 1616178600.0  
    }
    
