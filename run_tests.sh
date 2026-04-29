#!/bin/bash
# Run all Selenium tests sequentially and collect results
# Usage: ./run_tests.sh

TEST_DIR="$(dirname "$0")/tests"
RESULTS_FILE="/tmp/test_results_$(date +%Y%m%d_%H%M%S).log"
PASS=0
FAIL=0
TOTAL=0
FAILED_TESTS=""

echo "========================================"
echo " One-HR Selenium Test Suite"
echo " Date: $(date)"
echo "========================================"
echo ""

for test in "$TEST_DIR"/test_*.py; do
    testname=$(basename "$test")
    TOTAL=$((TOTAL + 1))
    echo "----------------------------------------"
    echo "[$TOTAL] Running: $testname"
    echo "----------------------------------------"
    
    if python3 "$test" 2>&1; then
        PASS=$((PASS + 1))
        echo ""
        echo "  RESULT: PASS"
    else
        FAIL=$((FAIL + 1))
        FAILED_TESTS="$FAILED_TESTS $testname"
        echo ""
        echo "  RESULT: FAIL"
    fi
    echo ""
done

echo "========================================"
echo " Test Summary"
echo "========================================"
echo " Total:  $TOTAL"
echo " Passed: $PASS"
echo " Failed: $FAIL"
if [ -n "$FAILED_TESTS" ]; then
    echo ""
    echo " Failed tests:$FAILED_TESTS"
fi
echo "========================================"
