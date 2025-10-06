import requests
import json
from datetime import datetime

BASE_URL = "http://34.116.176.94:8080/api/v1"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

class APITester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.created_ids = {
            'clients': [],
            'trainers': [],
            'services': [],
            'exercises': [],
            'memberships': [],
            'equipment': [],
            'workout_programs': [],
            'schedules': [],
            'trainer_schedules': []
        }
    
    def test(self, method, url, data=None, expected_status=None, allow_404=False):
        try:
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)
            elif method == "PUT":
                response = requests.put(url, json=data, timeout=10)
            elif method == "PATCH":
                response = requests.patch(url, json=data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, json=data, timeout=10)
            
            status = response.status_code
            
            if allow_404 and status == 404:
                success = True
            elif expected_status:
                success = status == expected_status
            else:
                success = status in [200, 201]
            
            if success:
                print(f"{Colors.GREEN}✅{Colors.RESET} {method:6} {url.split('/api/v1/')[-1]:50} → {status}")
                self.passed += 1
                return response
            else:
                print(f"{Colors.RED}❌{Colors.RESET} {method:6} {url.split('/api/v1/')[-1]:50} → {status} (Expected: {expected_status or '200/201'})")
                self.failed += 1
                return None
        except Exception as e:
            print(f"{Colors.RED}❌{Colors.RESET} {method:6} {url.split('/api/v1/')[-1]:50} → ERROR: {str(e)[:50]}")
            self.failed += 1
            return None
    
    def get_first_existing_id(self, endpoint):
        """Отримати перший існуючий ID з бази"""
        try:
            response = requests.get(f"{BASE_URL}/{endpoint}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    keys = list(data[0].keys())
                    id_key = [k for k in keys if 'id' in k.lower()][0]
                    return data[0][id_key]
        except:
            pass
        return 1
    
    def run_tests(self):
        print(f"\n{Colors.BLUE}{'='*80}{Colors.RESET}")
        print(f"{Colors.BLUE}🧪 Smart API Test Suite - All Endpoints with Dynamic IDs{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*80}{Colors.RESET}\n")
        
        # ============ CLIENTS ============
        print(f"\n{Colors.CYAN}{'─'*80}{Colors.RESET}")
        print(f"{Colors.YELLOW}📋 CLIENTS Endpoints{Colors.RESET}")
        print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
        
        self.test("GET", f"{BASE_URL}/clients")
        existing_client_id = self.get_first_existing_id("clients")
        self.test("GET", f"{BASE_URL}/clients/{existing_client_id}")
        
        resp = self.test("POST", f"{BASE_URL}/clients", {
            "name": "AutoTest",
            "surname": "Client",
            "phone_number": "1234567890",
            "trainer_id": 1
        }, 201)
        if resp:
            try:
                new_id = resp.json().get('client_id')
                if new_id:
                    self.created_ids['clients'].append(new_id)
                    self.test("PUT", f"{BASE_URL}/clients/{new_id}", {
                        "name": "Updated",
                        "surname": "Client",
                        "phone_number": "9999999999",
                        "trainer_id": 1
                    })
                    self.test("PATCH", f"{BASE_URL}/clients/{new_id}", {
                        "phone_number": "8888888888"
                    })
                    self.test("DELETE", f"{BASE_URL}/clients/{new_id}")
            except:
                pass
        
        # ============ TRAINERS ============
        print(f"\n{Colors.CYAN}{'─'*80}{Colors.RESET}")
        print(f"{Colors.YELLOW}👨‍🏫 TRAINERS Endpoints{Colors.RESET}")
        print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
        
        self.test("GET", f"{BASE_URL}/trainers")
        existing_trainer_id = self.get_first_existing_id("trainers")
        self.test("GET", f"{BASE_URL}/trainers/{existing_trainer_id}")
        self.test("GET", f"{BASE_URL}/trainers/{existing_trainer_id}/clients")
        
        resp = self.test("POST", f"{BASE_URL}/trainers", {
            "name": "AutoTest",
            "surname": "Trainer",
            "phone_number": "5555555555"
        }, 201)
        if resp:
            try:
                new_id = resp.json().get('trainer_id')
                if new_id:
                    self.created_ids['trainers'].append(new_id)
                    self.test("PUT", f"{BASE_URL}/trainers/{new_id}", {
                        "name": "Updated",
                        "surname": "Trainer",
                        "phone_number": "6666666666"
                    })
                    self.test("DELETE", f"{BASE_URL}/trainers/{new_id}")
            except:
                pass
        
        # ============ SERVICES ============
        print(f"\n{Colors.CYAN}{'─'*80}{Colors.RESET}")
        print(f"{Colors.YELLOW}🛠️ SERVICES Endpoints{Colors.RESET}")
        print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
        
        self.test("GET", f"{BASE_URL}/services")
        existing_service_id = self.get_first_existing_id("services")
        self.test("GET", f"{BASE_URL}/services/{existing_service_id}")
        self.test("GET", f"{BASE_URL}/services/stats?table_name=services&column_name=price&operation=AVG", allow_404=True)
        
        resp = self.test("POST", f"{BASE_URL}/services", {
            "service_name": "AutoTest Service",
            "price": 99.99
        }, 201)
        if resp:
            try:
                new_id = resp.json().get('service_id')
                if new_id:
                    self.created_ids['services'].append(new_id)
                    self.test("PUT", f"{BASE_URL}/services/{new_id}", {
                        "service_name": "Updated Service",
                        "price": 199.99
                    })
                    self.test("DELETE", f"{BASE_URL}/services/{new_id}")
            except:
                pass
        
        # ============ EXERCISES ============
        print(f"\n{Colors.CYAN}{'─'*80}{Colors.RESET}")
        print(f"{Colors.YELLOW}💪 EXERCISES Endpoints{Colors.RESET}")
        print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
        
        self.test("GET", f"{BASE_URL}/exercises")
        existing_exercise_id = self.get_first_existing_id("exercises")
        self.test("GET", f"{BASE_URL}/exercises/{existing_exercise_id}")
        self.test("GET", f"{BASE_URL}/exercises/{existing_exercise_id}/equipment", allow_404=True)
        
        resp = self.test("POST", f"{BASE_URL}/exercises", {
            "exercise_name": "AutoTest Exercise",
            "workout_program_id": 1
        }, 201)
        if resp:
            try:
                new_id = resp.json().get('exercise_id')
                if new_id:
                    self.created_ids['exercises'].append(new_id)
                    self.test("PUT", f"{BASE_URL}/exercises/{new_id}", {
                        "exercise_name": "Updated Exercise",
                        "workout_program_id": 1
                    })
                    self.test("DELETE", f"{BASE_URL}/exercises/{new_id}")
            except:
                pass
        
        # ============ MEMBERSHIPS ============
        print(f"\n{Colors.CYAN}{'─'*80}{Colors.RESET}")
        print(f"{Colors.YELLOW}🎟️ MEMBERSHIPS Endpoints{Colors.RESET}")
        print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
        
        self.test("GET", f"{BASE_URL}/memberships")
        existing_membership_id = self.get_first_existing_id("memberships")
        self.test("GET", f"{BASE_URL}/memberships/{existing_membership_id}")
        
        resp = self.test("POST", f"{BASE_URL}/memberships", {
            "client_id": existing_client_id,
            "membership_type": "Premium",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31"
        }, 201)
        if resp:
            try:
                new_id = resp.json().get('membership_id')
                if new_id:
                    self.created_ids['memberships'].append(new_id)
                    self.test("PUT", f"{BASE_URL}/memberships/{new_id}", {
                        "client_id": existing_client_id,
                        "membership_type": "Gold",
                        "start_date": "2025-01-01",
                        "end_date": "2025-12-31"
                    })
                    self.test("DELETE", f"{BASE_URL}/memberships/{new_id}")
            except:
                pass
        
        # ============ EQUIPMENT ============
        print(f"\n{Colors.CYAN}{'─'*80}{Colors.RESET}")
        print(f"{Colors.YELLOW}🏋️ EQUIPMENT Endpoints{Colors.RESET}")
        print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
        
        self.test("GET", f"{BASE_URL}/equipment")
        existing_equipment_id = self.get_first_existing_id("equipment")
        self.test("GET", f"{BASE_URL}/equipment/{existing_equipment_id}")
        
        resp = self.test("POST", f"{BASE_URL}/equipment", {
            "equipment_name": "AutoTest Equipment"
        }, 201)
        if resp:
            try:
                new_id = resp.json().get('equipment_id')
                if new_id:
                    self.created_ids['equipment'].append(new_id)
                    self.test("PUT", f"{BASE_URL}/equipment/{new_id}", {
                        "equipment_name": "Updated Equipment"
                    })
                    self.test("DELETE", f"{BASE_URL}/equipment/{new_id}")
            except:
                pass
        
        # ============ WORKOUT PROGRAMS ============
        print(f"\n{Colors.CYAN}{'─'*80}{Colors.RESET}")
        print(f"{Colors.YELLOW}📋 WORKOUT PROGRAMS Endpoints{Colors.RESET}")
        print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
        
        self.test("GET", f"{BASE_URL}/workout-programs")
        existing_program_id = self.get_first_existing_id("workout-programs")
        self.test("GET", f"{BASE_URL}/workout-programs/{existing_program_id}")
        
        resp = self.test("POST", f"{BASE_URL}/workout-programs", {
            "program_name": "AutoTest Program",
            "trainer_id": existing_trainer_id
        }, 201)
        if resp:
            try:
                new_id = resp.json().get('workout_program_id')
                if new_id:
                    self.created_ids['workout_programs'].append(new_id)
                    self.test("PUT", f"{BASE_URL}/workout-programs/{new_id}", {
                        "program_name": "Updated Program",
                        "trainer_id": existing_trainer_id
                    })
                    self.test("DELETE", f"{BASE_URL}/workout-programs/{new_id}")
            except:
                pass
        
        # ============ EXERCISE-EQUIPMENT ============
        print(f"\n{Colors.CYAN}{'─'*80}{Colors.RESET}")
        print(f"{Colors.YELLOW}🔗 EXERCISE-EQUIPMENT Relations{Colors.RESET}")
        print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
        
        self.test("GET", f"{BASE_URL}/exercise-equipment")
        self.test("GET", f"{BASE_URL}/exercise-equipment/equipment/{existing_equipment_id}/exercises", allow_404=True)
        self.test("GET", f"{BASE_URL}/exercise-equipment/exercises-with-equipment")
        
        self.test("POST", f"{BASE_URL}/exercise-equipment", {
            "exercise_id": existing_exercise_id,
            "equipment_id": existing_equipment_id
        }, 201)
        self.test("DELETE", f"{BASE_URL}/exercise-equipment", {
            "exercise_id": existing_exercise_id,
            "equipment_id": existing_equipment_id
        })
        
        # ============ SCHEDULES ============
        print(f"\n{Colors.CYAN}{'─'*80}{Colors.RESET}")
        print(f"{Colors.YELLOW}📅 SCHEDULES Endpoints{Colors.RESET}")
        print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
        
        self.test("GET", f"{BASE_URL}/schedules")
        existing_schedule_id = self.get_first_existing_id("schedules")
        self.test("GET", f"{BASE_URL}/schedules/{existing_schedule_id}")
        
        resp = self.test("POST", f"{BASE_URL}/schedules", {
            "service_id": existing_service_id,
            "day_of_week": "Monday",
            "open_time": "09:00:00",
            "close_time": "18:00:00"
        }, 201)
        if resp:
            try:
                new_id = resp.json().get('schedule_id')
                if new_id:
                    self.created_ids['schedules'].append(new_id)
                    self.test("PUT", f"{BASE_URL}/schedules/{new_id}", {
                        "service_id": existing_service_id,
                        "day_of_week": "Tuesday",
                        "open_time": "10:00:00",
                        "close_time": "19:00:00"
                    })
                    self.test("DELETE", f"{BASE_URL}/schedules/{new_id}")
            except:
                pass
        
        # ============ TRAINER SCHEDULES ============
        print(f"\n{Colors.CYAN}{'─'*80}{Colors.RESET}")
        print(f"{Colors.YELLOW}🗓️ TRAINER SCHEDULES Endpoints{Colors.RESET}")
        print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
        
        self.test("GET", f"{BASE_URL}/trainer-schedules")
        existing_trainer_schedule_id = self.get_first_existing_id("trainer-schedules")
        self.test("GET", f"{BASE_URL}/trainer-schedules/{existing_trainer_schedule_id}")
        
        resp = self.test("POST", f"{BASE_URL}/trainer-schedules", {
            "trainer_id": existing_trainer_id,
            "day_of_week": "Wednesday"
        }, 201)
        if resp:
            try:
                new_id = resp.json().get('schedule_id')
                if new_id:
                    self.created_ids['trainer_schedules'].append(new_id)
                    self.test("PUT", f"{BASE_URL}/trainer-schedules/{new_id}", {
                        "trainer_id": existing_trainer_id,
                        "day_of_week": "Thursday"
                    })
                    self.test("DELETE", f"{BASE_URL}/trainer-schedules/{new_id}")
            except:
                pass
        
        # ============ RESULTS ============
        self.print_results()
    
    def print_results(self):
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BLUE}{'='*80}{Colors.RESET}")
        print(f"{Colors.GREEN}✅ Passed: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}❌ Failed: {self.failed}{Colors.RESET}")
        print(f"{Colors.CYAN}📊 Pass Rate: {pass_rate:.1f}%{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*80}{Colors.RESET}\n")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": total,
            "passed": self.passed,
            "failed": self.failed,
            "pass_rate": f"{pass_rate:.1f}%",
            "created_ids": self.created_ids
        }
        
        with open("test_results_smart.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"📊 Results saved to test_results_smart.json\n")

if __name__ == "__main__":
    tester = APITester()
    tester.run_tests()
