import requests

BASE_URL = "http://localhost:8000"

def verify_filters():
    print("Verifying Search Filters & Data Accuracy...")

    # 1. Verify Location Filter (California)
    print("\nTesting State Filter (CA)...")
    r = requests.get(f"{BASE_URL}/colleges/?state=CA")
    if r.status_code == 200:
        data = r.json()
        print(f"Found {len(data)} colleges in CA.")
        names = [c['name'] for c in data]
        print(f"Names: {names}")
        
        expected = ["Stanford University", "University of California, Berkeley", "University of California, Los Angeles"]
        # Allow partial match or strict
        if all(any(e in n for n in names) for e in expected):
            print("✅ CA Filter Passed: Top CA schools found.")
        else:
            print("❌ CA Filter Failed: Missing top schools.")

        # Negative Check
        if "Massachusetts Institute of Technology" in names:
             print("❌ CA Filter Failed: Found MIT (MA) in CA search!")
        else:
             print("✅ CA Filter Strictness Passed: No MA schools in CA.")

    # 1.5 Verify MA Filter (should find MIT, Harvard, BU)
    print("\nTesting State Filter (MA)...")
    r = requests.get(f"{BASE_URL}/colleges/?state=MA")
    data = r.json()
    names = [c['name'] for c in data]
    print(f"Names: {names}")
    expected_ma = ["Massachusetts Institute of Technology", "Harvard University"]
    if all(e in names for e in expected_ma):
        print("✅ MA Filter Passed.")
    else:
        print("❌ MA Filter Failed.")

    # 2. Verify Cost Filter (Max $40k)
    print("\nTesting Cost Filter (Max $40k)...")
    r = requests.get(f"{BASE_URL}/colleges/?max_cost=40000")
    data = r.json()
    print(f"Found {len(data)} cheaper colleges.")
    for c in data:
        if c['avg_cost'] > 40000:
            print(f"❌ Cost Filter Failed: {c['name']} costs {c['avg_cost']}")
    
    # Check if UCLA/Berkeley/Florida/Michigan are here (all public)
    names = [c['name'] for c in data]
    publics = ["University of Florida", "University of Michigan", "University of California, Los Angeles"]
    if any(p in names for p in publics):
         print(f"✅ Cost Filter Passed: Public universities found.")

    # 3. Verify Admission Rate (Max 10%)
    print("\nTesting Selectivity Filter (Max 10%)...")
    r = requests.get(f"{BASE_URL}/colleges/?max_admission_rate=0.10")
    data = r.json()
    print(f"Found {len(data)} highly selective colleges.")
    names = [c['name'] for c in data]
    print(f"Names: {names}")
    
    ivies = ["Harvard University", "Stanford University", "Columbia University", "Massachusetts Institute of Technology"]
    if all(i in names for i in ivies):
        print("✅ Selectivity Filter Passed: Ivies/Stanford found.")
    else:
        print("❌ Selectivity Filter Failed.")

if __name__ == "__main__":
    verify_filters()
