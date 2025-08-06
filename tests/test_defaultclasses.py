from fxdc import dumps, loads
from fxdc.defaultclasses.pandasdefaults import data_frame_to_data


def test_python_defaults():
    # Test default Python types
    data = {
        "Bytes": b"Hi",
        "Set": {1, 2, 3},
        "Range": range(1, 3),  
        "Tuple": (1, 2, 3),
    }
    print("Original Data:", data)
    serialized_data = dumps(data)
    print("Serialized Data:", serialized_data)
    loaded_data = loads(serialized_data).original
    print("Loaded Data:", loaded_data)
    assert loaded_data == data, "Loaded data does not match original data"
    
def test_datetime_defaults():
    from datetime import datetime, date, time, timedelta
    # Test default datetime types
    data = {
        "datetime": datetime(2023, 10, 1, 12, 0, 0),
        "date": date(2023, 10, 1),
        "time": time(12, 0, 0),
        "timedelta": timedelta(days=1, hours=2, minutes=30),
    }
    print("Original Data:", data)
    serialized_data = dumps(data)
    print("Serialized Data:", serialized_data)
    loaded_data = loads(serialized_data).original
    print("Loaded Data:", loaded_data)
    assert loaded_data == data, "Loaded data does not match original data"
    
def test_numpy_defaults():
    try:
        import numpy as np
    except ImportError:
        print("Numpy not found, skipping numpy defaults test")
        return
    
    # Test default numpy types
    data = {
        "ndarray": np.array([1, 2, 3]),
        "matrix": np.matrix([[1, 2], [3, 4]]),
    }
    
    
    print("Original Data:", data)
    serialized_data = dumps(data)
    print("Serialized Data:", serialized_data)
    loaded_data = loads(serialized_data).original
    print("Loaded Data:", loaded_data)
    assert data["ndarray"].tolist() == loaded_data["ndarray"].tolist(), "Loaded data does not match original data"
    assert data["matrix"].tolist() == loaded_data["matrix"].tolist(), "Loaded data does not match original data"

def test_pandas_defaults():
    try:
        import pandas as pd
    except ImportError:
        print("Pandas not found, skipping pandas defaults test")
        return
    
    # Test default pandas types
    data = {
        "dataframe": pd.DataFrame({"A": [1, 2], "B": [3, 4]}),
    }
    print("data_frame_to_data:", data_frame_to_data(data["dataframe"]))
    
    # Ensure the DataFrame is serialized and deserialized correctly
    print("Original Data:", data)
    serialized_data = dumps(data)
    print("Serialized Data:", serialized_data)
    loaded_data = loads(serialized_data).original
    print("Loaded Data:", loaded_data)
    assert data["dataframe"].equals(loaded_data["dataframe"]), "Loaded data does not match original data"
    