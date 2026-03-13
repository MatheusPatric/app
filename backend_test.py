#!/usr/bin/env python3
"""
Backend API Testing for Proposal Generator
Tests all CRUD operations for the proposals API endpoints
"""

import requests
import json
import sys
import os
from datetime import datetime

# Get base URL from environment or use default
BASE_URL = os.getenv('NEXT_PUBLIC_BASE_URL', 'https://client-deck.preview.emergentagent.com')
API_BASE = f"{BASE_URL}/api"

# Test data as specified in the review request
TEST_PROPOSAL = {
    "clientName": "João Silva",
    "companyName": "Tech Solutions LTDA", 
    "title": "Proposta de Gestão de Conteúdo para Mídias Digitais",
    "description": "Estratégia completa para crescimento nas redes sociais",
    "strategyOverview": "Nossa estratégia foca em posicionamento digital e humanização da marca",
    "plans": [
        {
            "name": "Plano Básico",
            "price": "R$ 2.500",
            "features": [
                "Planejamento estratégico mensal",
                "Gestão do Instagram", 
                "10 conteúdos mensais"
            ]
        }
    ],
    "brandName": "Agência Digital",
    "contactEmail": "contato@agencia.com",
    "contactWhatsApp": "11999999999"
}

def print_test_result(test_name, success, message="", response_data=None):
    """Print formatted test results"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if message:
        print(f"   {message}")
    if response_data and not success:
        print(f"   Response: {response_data}")
    print()

def test_get_all_proposals_empty():
    """Test GET /api/proposals - should return empty array initially"""
    try:
        print("🧪 Testing GET /api/proposals (empty state)...")
        response = requests.get(f"{API_BASE}/proposals", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'proposals' in data and isinstance(data['proposals'], list):
                print_test_result("GET /api/proposals (empty)", True, 
                                f"Status: {response.status_code}, Found {len(data['proposals'])} proposals")
                return True
            else:
                print_test_result("GET /api/proposals (empty)", False, 
                                "Response missing 'proposals' array", data)
                return False
        else:
            print_test_result("GET /api/proposals (empty)", False, 
                            f"Expected 200, got {response.status_code}", response.text)
            return False
            
    except Exception as e:
        print_test_result("GET /api/proposals (empty)", False, f"Exception: {str(e)}")
        return False

def test_create_proposal():
    """Test POST /api/proposals - create a new proposal"""
    try:
        print("🧪 Testing POST /api/proposals...")
        response = requests.post(
            f"{API_BASE}/proposals",
            json=TEST_PROPOSAL,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            if 'proposal' in data:
                proposal = data['proposal']
                # Check if required fields are present
                required_fields = ['id', 'createdAt', 'updatedAt']
                missing_fields = [field for field in required_fields if field not in proposal]
                
                if not missing_fields:
                    print_test_result("POST /api/proposals", True, 
                                    f"Status: {response.status_code}, ID: {proposal['id']}")
                    return proposal['id']  # Return the ID for subsequent tests
                else:
                    print_test_result("POST /api/proposals", False, 
                                    f"Missing fields: {missing_fields}", data)
                    return None
            else:
                print_test_result("POST /api/proposals", False, 
                                "Response missing 'proposal' object", data)
                return None
        else:
            print_test_result("POST /api/proposals", False, 
                            f"Expected 201, got {response.status_code}", response.text)
            return None
            
    except Exception as e:
        print_test_result("POST /api/proposals", False, f"Exception: {str(e)}")
        return None

def test_get_single_proposal(proposal_id):
    """Test GET /api/proposals/{id} - get single proposal"""
    try:
        print(f"🧪 Testing GET /api/proposals/{proposal_id}...")
        response = requests.get(f"{API_BASE}/proposals/{proposal_id}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'proposal' in data:
                proposal = data['proposal']
                if proposal['id'] == proposal_id:
                    print_test_result("GET /api/proposals/{id}", True, 
                                    f"Status: {response.status_code}, Retrieved proposal with ID: {proposal_id}")
                    return True
                else:
                    print_test_result("GET /api/proposals/{id}", False, 
                                    f"ID mismatch: expected {proposal_id}, got {proposal['id']}")
                    return False
            else:
                print_test_result("GET /api/proposals/{id}", False, 
                                "Response missing 'proposal' object", data)
                return False
        else:
            print_test_result("GET /api/proposals/{id}", False, 
                            f"Expected 200, got {response.status_code}", response.text)
            return False
            
    except Exception as e:
        print_test_result("GET /api/proposals/{id}", False, f"Exception: {str(e)}")
        return False

def test_get_nonexistent_proposal():
    """Test GET /api/proposals/{id} - should return 404 for non-existent ID"""
    try:
        fake_id = "nonexistent-id-12345"
        print(f"🧪 Testing GET /api/proposals/{fake_id} (404 test)...")
        response = requests.get(f"{API_BASE}/proposals/{fake_id}", timeout=10)
        
        if response.status_code == 404:
            print_test_result("GET /api/proposals/{id} (404)", True, 
                            f"Status: {response.status_code} - Correctly returned 404 for non-existent ID")
            return True
        else:
            print_test_result("GET /api/proposals/{id} (404)", False, 
                            f"Expected 404, got {response.status_code}", response.text)
            return False
            
    except Exception as e:
        print_test_result("GET /api/proposals/{id} (404)", False, f"Exception: {str(e)}")
        return False

def test_update_proposal(proposal_id):
    """Test PUT /api/proposals/{id} - update proposal"""
    try:
        print(f"🧪 Testing PUT /api/proposals/{proposal_id}...")
        
        # Updated data
        updated_data = {
            **TEST_PROPOSAL,
            "title": "Updated Proposal Title",
            "description": "Updated description for the proposal",
            "plans": [
                {
                    "name": "Plano Premium",
                    "price": "R$ 3.500",
                    "features": [
                        "Planejamento estratégico mensal",
                        "Gestão do Instagram e Facebook",
                        "15 conteúdos mensais",
                        "Relatórios mensais"
                    ]
                }
            ]
        }
        
        response = requests.put(
            f"{API_BASE}/proposals/{proposal_id}",
            json=updated_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'proposal' in data:
                proposal = data['proposal']
                if (proposal['id'] == proposal_id and 
                    proposal['title'] == updated_data['title'] and
                    'createdAt' in proposal and 'updatedAt' in proposal):
                    print_test_result("PUT /api/proposals/{id}", True, 
                                    f"Status: {response.status_code}, Updated proposal successfully")
                    return True
                else:
                    print_test_result("PUT /api/proposals/{id}", False, 
                                    "Update validation failed", proposal)
                    return False
            else:
                print_test_result("PUT /api/proposals/{id}", False, 
                                "Response missing 'proposal' object", data)
                return False
        else:
            print_test_result("PUT /api/proposals/{id}", False, 
                            f"Expected 200, got {response.status_code}", response.text)
            return False
            
    except Exception as e:
        print_test_result("PUT /api/proposals/{id}", False, f"Exception: {str(e)}")
        return False

def test_delete_proposal(proposal_id):
    """Test DELETE /api/proposals/{id} - delete proposal"""
    try:
        print(f"🧪 Testing DELETE /api/proposals/{proposal_id}...")
        response = requests.delete(f"{API_BASE}/proposals/{proposal_id}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'message' in data:
                print_test_result("DELETE /api/proposals/{id}", True, 
                                f"Status: {response.status_code}, {data['message']}")
                return True
            else:
                print_test_result("DELETE /api/proposals/{id}", False, 
                                "Response missing success message", data)
                return False
        else:
            print_test_result("DELETE /api/proposals/{id}", False, 
                            f"Expected 200, got {response.status_code}", response.text)
            return False
            
    except Exception as e:
        print_test_result("DELETE /api/proposals/{id}", False, f"Exception: {str(e)}")
        return False

def test_get_deleted_proposal(proposal_id):
    """Test GET /api/proposals/{id} - should return 404 after deletion"""
    try:
        print(f"🧪 Testing GET /api/proposals/{proposal_id} (after deletion)...")
        response = requests.get(f"{API_BASE}/proposals/{proposal_id}", timeout=10)
        
        if response.status_code == 404:
            print_test_result("GET /api/proposals/{id} (after deletion)", True, 
                            f"Status: {response.status_code} - Correctly returned 404 after deletion")
            return True
        else:
            print_test_result("GET /api/proposals/{id} (after deletion)", False, 
                            f"Expected 404, got {response.status_code}", response.text)
            return False
            
    except Exception as e:
        print_test_result("GET /api/proposals/{id} (after deletion)", False, f"Exception: {str(e)}")
        return False

def main():
    """Run all backend API tests"""
    print("=" * 80)
    print("🚀 PROPOSAL GENERATOR API TESTING")
    print("=" * 80)
    print(f"Testing API at: {API_BASE}")
    print(f"Database: proposal_generator")
    print(f"Collection: proposals")
    print("=" * 80)
    
    test_results = []
    proposal_id = None
    
    # Test 1: GET all proposals (empty state)
    test_results.append(test_get_all_proposals_empty())
    
    # Test 2: POST create proposal
    proposal_id = test_create_proposal()
    test_results.append(proposal_id is not None)
    
    if proposal_id:
        # Test 3: GET single proposal
        test_results.append(test_get_single_proposal(proposal_id))
        
        # Test 4: GET non-existent proposal (404)
        test_results.append(test_get_nonexistent_proposal())
        
        # Test 5: PUT update proposal
        test_results.append(test_update_proposal(proposal_id))
        
        # Test 6: DELETE proposal
        test_results.append(test_delete_proposal(proposal_id))
        
        # Test 7: GET deleted proposal (404)
        test_results.append(test_get_deleted_proposal(proposal_id))
    else:
        print("⚠️  Skipping remaining tests due to failed proposal creation")
        test_results.extend([False] * 5)  # Mark remaining tests as failed
    
    # Summary
    print("=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check the details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())