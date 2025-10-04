import requests
import json

BASE_URL = "http://34.116.176.94:8080/api/v1"

# Визначаємо всі endpoints
endpoints = {
    "clients": ["", "/1"],
    "trainers": ["", "/1", "/1/clients"],
    "services": ["", "/1"],
    "exercises": ["", "/1", "/1/equipment"],
    "memberships": ["", "/1"],
    "equipment": ["", "/1"],
    "workout-programs": ["", "/1"],
    "exercise-equipment": ["", "/equipment/1/exercises", "/exercises-with-equipment"],
    "schedules": ["", "/1"],
    "trainer-schedules": ["", "/1"]
}

def test_get_endpoints():
    """Тестує всі GET endpoints"""
    failed = []
    passed = []
    
    for resource, paths in endpoints.items():
        for path in paths:
            url = f"{BASE_URL}/{resource}{path}"
            try:
                response = requests.get(url, timeout=5)
                status = response.status_code
                
                if status == 500:
                    failed.append({
                        "url": url,
                        "status": status,
                        "error": response.text[:200]
                    })
                    print(f"❌ FAIL: {url} - Status {status}")
                else:
                    passed.append(url)
                    print(f"✅ PASS: {url} - Status {status}")
            except Exception as e:
                failed.append({
                    "url": url,
                    "error": str(e)
                })
                print(f"⚠️  ERROR: {url} - {str(e)}")
    
    print("\n" + "="*50)
    print(f"✅ Passed: {len(passed)}")
    print(f"❌ Failed: {len(failed)}")
    print("="*50)
    
    if failed:
        print("\n❌ Failed endpoints:")
        for item in failed:
            print(f"  - {item['url']}")
            if 'error' in item and len(item['error']) < 100:
                print(f"    Error: {item['error']}")
    
    return failed, passed

if __name__ == "__main__":
    print("🧪 Testing all API endpoints...\n")
    failed, passed = test_get_endpoints()
    
    # Зберегти результати
    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            "passed": passed,
            "failed": failed,
            "total": len(passed) + len(failed),
            "pass_rate": f"{len(passed)/(len(passed)+len(failed))*100:.1f}%"
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Results saved to test_results.json")
