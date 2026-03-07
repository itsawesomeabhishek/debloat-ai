import timeit
import time
from unittest.mock import MagicMock
from openclaw_integration import ActionExecutor

def benchmark():
    mock_adb = MagicMock()
    # Generate 10000 mock packages
    mock_packages = [{'packageName': f'com.example.app{i}'} for i in range(10000)]
    mock_adb.list_packages.return_value = mock_packages

    executor = ActionExecutor(mock_adb)

    # Target keywords that will cause fuzzy matching
    # Some match, some don't
    entities = {
        'target': 'facebook instagram whatsapp',
        'packages': ['facebook', 'instagram', 'whatsapp', 'notfound']
    }

    # Run the function a few times to measure execution time
    start = time.time()
    for _ in range(100):
        executor._handle_uninstall(entities)
    end = time.time()

    duration = end - start
    print(f"Execution time for 100 runs: {duration:.4f} seconds")

if __name__ == '__main__':
    benchmark()
