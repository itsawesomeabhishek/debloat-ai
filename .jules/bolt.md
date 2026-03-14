## 2024-05-24 - React List Rendering Bottleneck
**Learning:** In a codebase dealing with potentially hundreds of items like Android packages, mapping inline components with complex styling and multiple child components inside a single `useState` array update causes severe render blocking.
**Action:** Always extract list items into separate components wrapped in `React.memo` and ensure callback references passed to them (like `toggleSelect`) are stabilized using `useCallback` and `useRef` to hold latest state without triggering re-renders of the parent function.
## 2024-05-24 - AI Package Scanning Bottleneck
**Learning:** Re-evaluating lists or compiling regexes on every package check in `_is_likely_bloatware` within the Python backend causes a significant performance overhead when scanning thousands of installed Android packages.
**Action:** Always extract static indicator arrays into class-level pre-compiled regex objects (`re.compile`) and exact-match exclusions into `frozenset` objects to achieve O(1) lookups and significantly faster substring matching.
## 2024-05-25 - Python String Parsing Overhead
**Learning:** In Python backend scripts (e.g., `adb_operations.py`), iterating over large command outputs using `str.split('\n')` and modifying strings with `.replace()` and `.split('.')` inside loops introduces measurable overhead due to intermediate list allocations.
**Action:** Always prefer `str.splitlines()` in list comprehensions combined with string slicing (e.g., `line[8:]`) and `str.find()` with slice indexing (`name[:dot_idx]`) for significantly faster string manipulation and parsing.
## 2024-05-25 - Python Class Instantiation Regex Overhead
**Learning:** Initializing dictionaries or lists with `re.compile()` within a class `__init__` method incurs unnecessary instantiation overhead when the class is created repeatedly, especially for stateless parsers like `CommandParser`. Furthermore, nested dictionary iterations (`items()`) inside `parse_command` add unnecessary complexity and slow down command processing compared to a single flat iteration list.
**Action:** Always extract static regular expressions and patterns to module-level constants. If multiple patterns belong to different intents, flatten them into a single list of tuples (e.g., `[(intent, pattern)]`) to enable faster O(n) single loop traversal and bypass `__init__` overhead entirely.
