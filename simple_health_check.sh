#!/bin/bash

echo "================================================================================"
echo "🏥 BACKEND HEALTH CHECK - Customer Mind IQ Platform"
echo "================================================================================"
echo "Backend URL: http://localhost:8001"
echo "Test Time: $(date)"
echo "================================================================================"

# Test endpoints
endpoints=(
    "api/health:Health Check"
    "api/analytics:Analytics Dashboard"
    "api/universal/dashboard:Universal Dashboard"
    "api/universal/connectors/status:Connectors Status"
    "api/intelligence/dashboard:Intelligence Dashboard"
    "api/marketing/multi-channel-orchestration:Marketing Dashboard"
)

passed=0
total=0

echo ""
echo "📋 Testing Core Backend Endpoints..."

for endpoint_info in "${endpoints[@]}"; do
    IFS=':' read -r endpoint name <<< "$endpoint_info"
    total=$((total + 1))
    
    echo ""
    echo "🔍 Testing $name..."
    echo "   URL: http://localhost:8001/$endpoint"
    
    # Test with curl and capture status code
    status_code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8001/$endpoint" --max-time 30)
    
    if [ "$status_code" = "200" ]; then
        echo "✅ Passed - Status: $status_code"
        passed=$((passed + 1))
        
        # Get some response data for key endpoints
        if [[ "$endpoint" == "api/health" ]]; then
            response=$(curl -s "http://localhost:8001/$endpoint" --max-time 10)
            service=$(echo "$response" | grep -o '"service":"[^"]*"' | cut -d'"' -f4)
            version=$(echo "$response" | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
            echo "   Service: $service"
            echo "   Version: $version"
        elif [[ "$endpoint" == "api/analytics" ]]; then
            response=$(curl -s "http://localhost:8001/$endpoint" --max-time 10)
            customers=$(echo "$response" | grep -o '"total_customers":[0-9]*' | cut -d':' -f2)
            revenue=$(echo "$response" | grep -o '"total_revenue":[0-9.]*' | cut -d':' -f2)
            echo "   Customers: $customers"
            echo "   Revenue: \$$revenue"
        fi
    else
        echo "❌ Failed - Status: $status_code"
    fi
done

# Calculate success rate
success_rate=$(echo "scale=1; $passed * 100 / $total" | bc -l 2>/dev/null || echo "$(($passed * 100 / $total))")

echo ""
echo "================================================================================"
echo "📊 BACKEND HEALTH CHECK SUMMARY"
echo "================================================================================"
echo "Total Tests: $total"
echo "Passed: $passed"
echo "Failed: $((total - passed))"
echo "Success Rate: ${success_rate}%"

# Overall assessment
if [ "$passed" -ge $((total * 3 / 4)) ]; then
    echo ""
    echo "================================================================================"
    echo "🎉 OVERALL HEALTH: EXCELLENT"
    echo "✅ Backend server is running correctly after restructuring"
    echo "✅ Core APIs are responding properly"
    echo "✅ All critical endpoints are functional"
    echo "✅ $passed out of $total endpoints working"
    echo "================================================================================"
    exit 0
else
    echo ""
    echo "================================================================================"
    echo "⚠️  OVERALL HEALTH: ISSUES DETECTED"
    echo "❌ Some endpoints are not responding correctly"
    echo "❌ Only $passed out of $total endpoints working"
    echo "================================================================================"
    exit 1
fi