import timeit
import random
from adb_operations import ADBOperations

def run_benchmark():
    adb = ADBOperations()

    packages = [
        "com.android.systemui",    # Dangerous
        "com.android.vending",     # Dangerous
        "com.google.android.gms",  # Expert
        "com.android.bluetooth",   # Expert
        "com.samsung.android.bixby",# Caution
        "com.xiaomi.finddevice",   # Caution
        "com.example.myapp",       # Safe
        "org.mozilla.firefox",     # Safe
        "net.example.game"         # Safe
    ]

    # Pre-generate a large list of calls
    test_packages = random.choices(packages, k=100000)

    def test_func():
        for pkg in test_packages:
            adb._determine_safety_level(pkg)
            adb._guess_package_type(pkg)
            adb._get_app_name(pkg)

    # Warmup
    test_func()

    # Run benchmark
    iterations = 50
    total_time = timeit.timeit(test_func, number=iterations)

    print(f"Total time for {iterations} iterations of 100,000 package classifications:")
    print(f"{total_time:.4f} seconds")
    print(f"Average time per 100,000 package classifications:")
    print(f"{total_time/iterations:.4f} seconds")

if __name__ == "__main__":
    run_benchmark()
