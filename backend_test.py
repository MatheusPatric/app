#!/usr/bin/env python3

import requests
import json
import base64
from io import BytesIO
from PIL import Image
import sys

# Configuration
BASE_URL = "https://client-deck.preview.emergentagent.com/api"

def create_test_image_base64():
    """Create a small test image and return as base64"""
    # Create a small 10x10 red image
    img = Image.new('RGB', (10, 10), color='red')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_data = buffer.getvalue()
    return f"data:image/png;base64,{base64.b64encode(img_data).decode()}"

def test_ai_generate_endpoint():
    """Test the AI generation endpoint with different field types"""
    print("\n=== Testing AI Generation Endpoint ===")
    
    # Test expectedResults generation
    try:
        print("\n1. Testing AI generation for expectedResults...")
        response = requests.post(f"{BASE_URL}/ai-generate", 
                               json={"fieldType": "expectedResults", "prompt": "Generate expected results"})
        
        if response.status_code == 200:
            data = response.json()
            if 'text' in data and data['text']:
                print("✅ PASS - expectedResults generation successful")
                print(f"Generated text preview: {data['text'][:100]}...")
            else:
                print("❌ FAIL - No text returned in response")
                return False
        else:
            print(f"❌ FAIL - Status: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL - Exception: {str(e)}")
        return False
    
    # Test customNotes generation
    try:
        print("\n2. Testing AI generation for customNotes...")
        response = requests.post(f"{BASE_URL}/ai-generate", 
                               json={"fieldType": "customNotes", "prompt": "Generate custom notes"})
        
        if response.status_code == 200:
            data = response.json()
            if 'text' in data and data['text']:
                print("✅ PASS - customNotes generation successful")
                print(f"Generated text preview: {data['text'][:100]}...")
            else:
                print("❌ FAIL - No text returned in response")
                return False
        else:
            print(f"❌ FAIL - Status: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL - Exception: {str(e)}")
        return False
    
    return True

def test_create_proposal_with_new_fields():
    """Test creating a proposal with all new fields including creatives and AI-generated content"""
    print("\n=== Testing Create Proposal with New Fields ===")
    
    try:
        # First generate AI content
        print("\n1. Generating AI content for proposal...")
        
        # Generate expectedResults
        expected_results_response = requests.post(f"{BASE_URL}/ai-generate", 
                                                json={"fieldType": "expectedResults"})
        if expected_results_response.status_code != 200:
            print(f"❌ FAIL - Could not generate expectedResults: {expected_results_response.text}")
            return None
            
        expected_results = expected_results_response.json()['text']
        
        # Generate customNotes
        custom_notes_response = requests.post(f"{BASE_URL}/ai-generate", 
                                            json={"fieldType": "customNotes"})
        if custom_notes_response.status_code != 200:
            print(f"❌ FAIL - Could not generate customNotes: {custom_notes_response.text}")
            return None
            
        custom_notes = custom_notes_response.json()['text']
        
        print("✅ AI content generated successfully")
        
        # Create test images
        main_creative = create_test_image_base64()
        carousel_creatives = [
            create_test_image_base64(),
            create_test_image_base64(),
            create_test_image_base64()
        ]
        
        # Create proposal with all new fields
        print("\n2. Creating proposal with new fields...")
        proposal_data = {
            "clientName": "João Silva",
            "companyName": "Tech Solutions LTDA",
            "title": "Proposta de Gestão de Conteúdo",
            "mainCreative": main_creative,
            "carouselCreatives": carousel_creatives,
            "expectedResults": expected_results,
            "customNotes": custom_notes,
            # Pre-filled Zeri Solutions data
            "brandName": "Zeri Solutions",
            "contactEmail": "zeriagencia@gmail.com",
            "contactWhatsApp": "5584991151503"
        }
        
        response = requests.post(f"{BASE_URL}/proposals", json=proposal_data)
        
        if response.status_code == 201:
            data = response.json()
            proposal = data['proposal']
            
            # Verify all fields are present
            required_fields = ['id', 'clientName', 'companyName', 'title', 'mainCreative', 
                             'carouselCreatives', 'expectedResults', 'customNotes', 
                             'brandName', 'contactEmail', 'contactWhatsApp', 'createdAt', 'updatedAt']
            
            missing_fields = [field for field in required_fields if field not in proposal]
            
            if not missing_fields:
                print("✅ PASS - Proposal created with all new fields")
                print(f"Proposal ID: {proposal['id']}")
                print(f"Main creative length: {len(proposal['mainCreative'])} chars")
                print(f"Carousel creatives count: {len(proposal['carouselCreatives'])}")
                print(f"Expected results length: {len(proposal['expectedResults'])} chars")
                print(f"Custom notes length: {len(proposal['customNotes'])} chars")
                print(f"Brand name: {proposal['brandName']}")
                return proposal['id']
            else:
                print(f"❌ FAIL - Missing fields: {missing_fields}")
                return None
        else:
            print(f"❌ FAIL - Status: {response.status_code}, Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ FAIL - Exception: {str(e)}")
        return None

def test_retrieve_proposal_with_new_fields(proposal_id):
    """Test retrieving a proposal and verify all new fields are present"""
    print("\n=== Testing Retrieve Proposal with New Fields ===")
    
    try:
        print(f"\n1. Retrieving proposal {proposal_id}...")
        response = requests.get(f"{BASE_URL}/proposals/{proposal_id}")
        
        if response.status_code == 200:
            data = response.json()
            proposal = data['proposal']
            
            # Verify all new fields are properly stored and retrieved
            checks = [
                ('mainCreative', 'data:image/png;base64,'),
                ('carouselCreatives', list),
                ('expectedResults', str),
                ('customNotes', str),
                ('brandName', 'Zeri Solutions'),
                ('contactEmail', 'zeriagencia@gmail.com'),
                ('contactWhatsApp', '5584991151503')
            ]
            
            all_passed = True
            for field, expected in checks:
                if field not in proposal:
                    print(f"❌ FAIL - Missing field: {field}")
                    all_passed = False
                elif isinstance(expected, str) and expected.startswith('data:image'):
                    if not proposal[field].startswith(expected):
                        print(f"❌ FAIL - {field} doesn't start with expected format")
                        all_passed = False
                    else:
                        print(f"✅ {field} format correct")
                elif isinstance(expected, type):
                    if not isinstance(proposal[field], expected):
                        print(f"❌ FAIL - {field} is not of type {expected}")
                        all_passed = False
                    else:
                        print(f"✅ {field} type correct ({len(proposal[field])} items)" if expected == list else f"✅ {field} type correct")
                elif isinstance(expected, str):
                    if proposal[field] != expected:
                        print(f"❌ FAIL - {field} value mismatch. Expected: {expected}, Got: {proposal[field]}")
                        all_passed = False
                    else:
                        print(f"✅ {field} value correct")
            
            if all_passed:
                print("✅ PASS - All new fields properly stored and retrieved")
                return True
            else:
                print("❌ FAIL - Some field validations failed")
                return False
        else:
            print(f"❌ FAIL - Status: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL - Exception: {str(e)}")
        return False

def test_update_proposal_with_creatives(proposal_id):
    """Test updating a proposal to modify carouselCreatives"""
    print("\n=== Testing Update Proposal with Creatives ===")
    
    try:
        print(f"\n1. Updating proposal {proposal_id} with new carousel creatives...")
        
        # Create new carousel creatives
        new_carousel_creatives = [
            create_test_image_base64(),
            create_test_image_base64(),
            create_test_image_base64(),
            create_test_image_base64()  # Adding one more image
        ]
        
        update_data = {
            "carouselCreatives": new_carousel_creatives,
            "title": "Updated Proposta de Gestão de Conteúdo"
        }
        
        response = requests.put(f"{BASE_URL}/proposals/{proposal_id}", json=update_data)
        
        if response.status_code == 200:
            data = response.json()
            proposal = data['proposal']
            
            # Verify the update worked correctly
            if (len(proposal['carouselCreatives']) == 4 and 
                proposal['title'] == "Updated Proposta de Gestão de Conteúdo"):
                print("✅ PASS - Proposal updated successfully")
                print(f"New carousel creatives count: {len(proposal['carouselCreatives'])}")
                print(f"Updated title: {proposal['title']}")
                return True
            else:
                print(f"❌ FAIL - Update verification failed")
                print(f"Carousel count: {len(proposal['carouselCreatives'])}, Title: {proposal['title']}")
                return False
        else:
            print(f"❌ FAIL - Status: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL - Exception: {str(e)}")
        return False

def test_upload_image_endpoint():
    """Test the upload image endpoint"""
    print("\n=== Testing Upload Image Endpoint ===")
    
    try:
        print("\n1. Testing image upload...")
        test_image = create_test_image_base64()
        
        response = requests.post(f"{BASE_URL}/upload-image", 
                               json={"imageData": test_image})
        
        if response.status_code == 200:
            data = response.json()
            if 'imageUrl' in data and data['imageUrl'] == test_image:
                print("✅ PASS - Image upload endpoint working correctly")
                return True
            else:
                print("❌ FAIL - Image URL not returned correctly")
                return False
        else:
            print(f"❌ FAIL - Status: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL - Exception: {str(e)}")
        return False

def main():
    """Run all tests for the updated proposal generator"""
    print("🚀 Starting Proposal Generator New Features Test Suite")
    print(f"Testing against: {BASE_URL}")
    
    test_results = []
    
    # Test 1: AI Generation Endpoint
    test_results.append(("AI Generation Endpoint", test_ai_generate_endpoint()))
    
    # Test 2: Upload Image Endpoint
    test_results.append(("Upload Image Endpoint", test_upload_image_endpoint()))
    
    # Test 3: Create Proposal with New Fields
    proposal_id = test_create_proposal_with_new_fields()
    test_results.append(("Create Proposal with New Fields", proposal_id is not None))
    
    if proposal_id:
        # Test 4: Retrieve Proposal with New Fields
        test_results.append(("Retrieve Proposal with New Fields", 
                           test_retrieve_proposal_with_new_fields(proposal_id)))
        
        # Test 5: Update Proposal with Creatives
        test_results.append(("Update Proposal with Creatives", 
                           test_update_proposal_with_creatives(proposal_id)))
    else:
        test_results.append(("Retrieve Proposal with New Fields", False))
        test_results.append(("Update Proposal with Creatives", False))
    
    # Print final results
    print("\n" + "="*60)
    print("🏁 FINAL TEST RESULTS")
    print("="*60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nSUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! New features are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())