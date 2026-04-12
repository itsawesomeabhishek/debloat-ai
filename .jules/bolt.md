## 2024-05-24 - React List Rendering Bottleneck
**Learning:** In a codebase dealing with potentially hundreds of items like Android packages, mapping inline components with complex styling and multiple child components inside a single `useState` array update causes severe render blocking.
**Action:** Always extract list items into separate components wrapped in `React.memo` and ensure callback references passed to them (like `toggleSelect`) are stabilized using `useCallback` and `useRef` to hold latest state without triggering re-renders of the parent function.
## 2024-05-24 - AI Package Scanning Bottleneck
**Learning:** Re-evaluating lists or compiling regexes on every package check in `_is_likely_bloatware` within the Python backend causes a significant performance overhead when scanning thousands of installed Android packages.
**Action:** Always extract static indicator arrays into class-level pre-compiled regex objects (`re.compile`) and exact-match exclusions into `frozenset` objects to achieve O(1) lookups and significantly faster substring matching.
## 2024-05-25 - Python String Parsing Overhead
**Learning:** In Python backend scripts (e.g., `adb_operations.py`), iterating over large command outputs using `str.split('\n')` and modifying strings with `.replace()` and `.split('.')` inside loops introduces measurable overhead due to intermediate list allocations.
**Action:** Always prefer `str.splitlines()` in list comprehensions combined with string slicing (e.g., `line[8:]`) and `str.find()` with slice indexing (`name[:dot_idx]`) for significantly faster string manipulation and parsing.
## 2024-05-26 - React Array Filter Bottleneck
**Learning:** In React components dealing with large lists (like `PackageList.tsx`), chaining multiple `Array.prototype.filter()` calls inside a `useEffect` hooked to frequent state changes (like checkbox toggles) causes a massive O(4n) re-calculation overhead and blocks the main thread.
**Action:** Always extract static base array stats into a single-pass O(n) loop inside a `useMemo` block hooked to the array itself, and then mix in dynamic fast-changing states (like selection counts) in a separate `useEffect`. Also, in search filters, evaluate O(1) checks (like exact matches on enum values) before expensive O(n) string manipulation checks like `toLowerCase().includes()`.
