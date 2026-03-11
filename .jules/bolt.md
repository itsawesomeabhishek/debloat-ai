## 2024-05-24 - React List Rendering Bottleneck
**Learning:** In a codebase dealing with potentially hundreds of items like Android packages, mapping inline components with complex styling and multiple child components inside a single `useState` array update causes severe render blocking.
**Action:** Always extract list items into separate components wrapped in `React.memo` and ensure callback references passed to them (like `toggleSelect`) are stabilized using `useCallback` and `useRef` to hold latest state without triggering re-renders of the parent function.
## 2024-05-24 - AI Package Scanning Bottleneck
**Learning:** Re-evaluating lists or compiling regexes on every package check in `_is_likely_bloatware` within the Python backend causes a significant performance overhead when scanning thousands of installed Android packages.
**Action:** Always extract static indicator arrays into class-level pre-compiled regex objects (`re.compile`) and exact-match exclusions into `frozenset` objects to achieve O(1) lookups and significantly faster substring matching.
