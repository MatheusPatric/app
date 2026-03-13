#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Proposal Template System
Tests the complete proposal template functionality as requested.
"""

import requests
import json
import sys
from datetime import datetime

# Get base URL from environment
BASE_URL = "https://client-deck.preview.emergentagent.com/api"

def print_test_result(test_name, success, details=""):
    """Print formatted test results"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"    {details}")
    print()

def test_create_proposal_with_template():
    """Test 1: Create New Proposal with Template - Verify template fields are properly stored"""
    print("🧪 TEST 1: Create New Proposal with Template")
    
    # Template data as defined in CreateProposalModal.js (lines 14-68)
    template_data = {
        "clientName": "Maria Santos",
        "companyName": "Beleza Natural LTDA",
        "title": "Proposta de Gestão de Conteúdo para Mídias Digitais",
        "description": "Estratégia completa de posicionamento digital e crescimento nas redes sociais",
        "strategyOverview": """Nossa estratégia foi desenvolvida para maximizar sua presença digital e criar conexão genuína com seu público.

Focamos em três pilares fundamentais:

• Posicionamento Digital: Construir uma identidade forte e reconhecível no ambiente digital
• Otimização de Perfil: Garantir que seu perfil comunique valor desde o primeiro contato
• Estratégia de Conteúdo: Criar conteúdos que engajam, educam e convertem
• Crescimento da Marca: Aumentar autoridade e reconhecimento no seu nicho

Trabalhamos com metodologia comprovada, análise constante de métricas e ajustes estratégicos para garantir os melhores resultados.""",
        "plans": [
            {
                "name": "Plano Essencial",
                "price": "R$ 2.500",
                "features": [
                    "Planejamento estratégico mensal",
                    "Gestão do Instagram",
                    "10 conteúdos mensais",
                    "Até 4 vídeos editados",
                    "Direcionamento de conteúdo para stories",
                    "Acompanhamento de engajamento",
                    "Reunião estratégica mensal"
                ]
            },
            {
                "name": "Plano Profissional",
                "price": "R$ 3.000",
                "features": [
                    "Tudo do plano Essencial",
                    "12 conteúdos mensais",
                    "Até 6 vídeos editados",
                    "Desenvolvimento e posicionamento digital",
                    "Estratégia e humanização da marca"
                ]
            }
        ],
        "mainCreative": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A",
        "carouselCreatives": [
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A",
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A",
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A"
        ],
        "expectedResults": "• Aumento de 30-50% no engajamento orgânico nas primeiras 8 semanas\n• Crescimento de 20-35% na base de seguidores mensalmente\n• Melhoria no posicionamento digital da marca no nicho\n• Maior reconhecimento e autoridade no mercado\n• Conversões aumentadas através de conteúdo estratégico",
        "customNotes": "Esta proposta foi elaborada considerando as necessidades específicas e o perfil do seu negócio. Todos os serviços são personalizáveis e adaptáveis conforme a evolução da parceria.\n\nNosso compromisso é com resultados reais e mensuráveis. Trabalhamos com transparência total, relatórios mensais e reuniões estratégicas para alinhamento contínuo.\n\nEstamos prontos para iniciar e transformar sua presença digital!",
        "brandName": "Zeri Solutions",
        "brandDescription": "A Agencia Zeri surgiu com o proposito de otimizar o tempo de empresários e trazer a tona a identidade dos seus negócios em nichos diversos!",
        "contactEmail": "zeriagencia@gmail.com",
        "contactPhone": "84991151503",
        "contactInstagram": "@zeriagencia",
        "contactWhatsApp": "5584991151503"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/proposals", json=template_data, timeout=10)
        
        if response.status_code == 201:
            proposal = response.json().get('proposal', {})
            
            # Verify template fields are properly stored
            checks = [
                (proposal.get('title') == template_data['title'], "Template title stored correctly"),
                (len(proposal.get('plans', [])) == 2, "Two default plans created"),
                (proposal.get('plans', [{}])[0].get('name') == "Plano Essencial", "Plano Essencial name correct"),
                (proposal.get('plans', [{}])[0].get('price') == "R$ 2.500", "Plano Essencial price correct"),
                (proposal.get('plans', [{}, {}])[1].get('name') == "Plano Profissional", "Plano Profissional name correct"),
                (proposal.get('plans', [{}, {}])[1].get('price') == "R$ 3.000", "Plano Profissional price correct"),
                (proposal.get('strategyOverview', '').startswith("Nossa estratégia foi desenvolvida"), "Strategy overview template stored"),
                (proposal.get('brandName') == "Zeri Solutions", "Pre-filled Zeri Solutions brand name"),
                (proposal.get('contactEmail') == "zeriagencia@gmail.com", "Pre-filled Zeri contact email"),
                (proposal.get('contactWhatsApp') == "5584991151503", "Pre-filled Zeri WhatsApp"),
                (proposal.get('mainCreative', '').startswith("data:image/jpeg"), "Main creative stored"),
                (len(proposal.get('carouselCreatives', [])) == 3, "Carousel creatives stored (3 images)"),
                (proposal.get('expectedResults', '').startswith("• Aumento de 30-50%"), "Expected results stored"),
                (proposal.get('customNotes', '').startswith("Esta proposta foi elaborada"), "Custom notes stored")
            ]
            
            all_passed = all(check[0] for check in checks)
            details = f"Status: {response.status_code}, ID: {proposal.get('id', 'N/A')}"
            
            if all_passed:
                print_test_result("Create proposal with template", True, details)
                return proposal.get('id')
            else:
                failed_checks = [check[1] for check in checks if not check[0]]
                print_test_result("Create proposal with template", False, f"{details}, Failed: {', '.join(failed_checks)}")
                return None
        else:
            print_test_result("Create proposal with template", False, f"Status: {response.status_code}, Response: {response.text}")
            return None
            
    except Exception as e:
        print_test_result("Create proposal with template", False, f"Exception: {str(e)}")
        return None

def test_create_proposal_with_custom_prices():
    """Test 2: Create Proposal with Custom Prices - Verify custom prices are saved correctly"""
    print("🧪 TEST 2: Create Proposal with Custom Prices")
    
    # Template data with modified prices as specified in review request
    custom_price_data = {
        "clientName": "João Silva",
        "companyName": "Tech Innovations LTDA",
        "title": "Proposta de Gestão de Conteúdo para Mídias Digitais",
        "plans": [
            {
                "name": "Plano Essencial",
                "price": "R$ 3.200",  # Modified from R$ 2.500
                "features": [
                    "Planejamento estratégico mensal",
                    "Gestão do Instagram",
                    "10 conteúdos mensais"
                ]
            },
            {
                "name": "Plano Profissional", 
                "price": "R$ 4.500",  # Modified from R$ 3.000
                "features": [
                    "Tudo do plano Essencial",
                    "12 conteúdos mensais",
                    "Até 6 vídeos editados"
                ]
            }
        ],
        "brandName": "Zeri Solutions",
        "contactEmail": "zeriagencia@gmail.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/proposals", json=custom_price_data, timeout=10)
        
        if response.status_code == 201:
            proposal = response.json().get('proposal', {})
            
            # Verify custom prices are saved correctly
            essencial_price = proposal.get('plans', [{}])[0].get('price')
            profissional_price = proposal.get('plans', [{}, {}])[1].get('price')
            
            custom_prices_correct = (
                essencial_price == "R$ 3.200" and 
                profissional_price == "R$ 4.500"
            )
            
            details = f"Status: {response.status_code}, Essencial: {essencial_price}, Profissional: {profissional_price}"
            print_test_result("Create proposal with custom prices", custom_prices_correct, details)
            return proposal.get('id') if custom_prices_correct else None
            
        else:
            print_test_result("Create proposal with custom prices", False, f"Status: {response.status_code}")
            return None
            
    except Exception as e:
        print_test_result("Create proposal with custom prices", False, f"Exception: {str(e)}")
        return None

def test_all_template_features_together():
    """Test 3: Verify All Template Features Work Together"""
    print("🧪 TEST 3: Verify All Template Features Work Together")
    
    # Complete template data with all features as specified in review request
    complete_data = {
        "clientName": "Maria Santos",
        "companyName": "Beleza Natural LTDA",
        "title": "Proposta de Gestão de Conteúdo para Mídias Digitais",
        "strategyOverview": """Nossa estratégia foi desenvolvida para maximizar sua presença digital e criar conexão genuína com seu público.

Focamos em três pilares fundamentais:

• Posicionamento Digital: Construir uma identidade forte e reconhecível no ambiente digital
• Otimização de Perfil: Garantir que seu perfil comunique valor desde o primeiro contato
• Estratégia de Conteúdo: Criar conteúdos que engajam, educam e convertem
• Crescimento da Marca: Aumentar autoridade e reconhecimento no seu nicho

Trabalhamos com metodologia comprovada, análise constante de métricas e ajustes estratégicos para garantir os melhores resultados.""",
        "plans": [
            {
                "name": "Plano Essencial",
                "price": "R$ 3.200",
                "features": [
                    "Planejamento estratégico mensal",
                    "Gestão do Instagram",
                    "10 conteúdos mensais"
                ]
            }
        ],
        "mainCreative": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A",
        "carouselCreatives": [
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A",
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A"
        ],
        "expectedResults": "• Aumento de 30-50% no engajamento orgânico nas primeiras 8 semanas\n• Crescimento de 20-35% na base de seguidores mensalmente\n• Melhoria no posicionamento digital da marca no nicho",
        "customNotes": "Esta proposta foi elaborada considerando as necessidades específicas e o perfil do seu negócio.",
        "brandName": "Zeri Solutions",
        "contactEmail": "zeriagencia@gmail.com"
    }
    
    try:
        # Create proposal
        response = requests.post(f"{BASE_URL}/proposals", json=complete_data, timeout=10)
        
        if response.status_code == 201:
            proposal = response.json().get('proposal', {})
            proposal_id = proposal.get('id')
            
            # Retrieve and verify all fields are correct
            get_response = requests.get(f"{BASE_URL}/proposals/{proposal_id}", timeout=10)
            
            if get_response.status_code == 200:
                retrieved_proposal = get_response.json().get('proposal', {})
                
                # Verify all template features
                checks = [
                    (retrieved_proposal.get('title') == complete_data['title'], "Template title"),
                    (retrieved_proposal.get('strategyOverview') == complete_data['strategyOverview'], "Strategy overview"),
                    (len(retrieved_proposal.get('plans', [])) == 1, "Plans count"),
                    (retrieved_proposal.get('plans', [{}])[0].get('price') == "R$ 3.200", "Custom price"),
                    (retrieved_proposal.get('mainCreative') == complete_data['mainCreative'], "Main creative"),
                    (len(retrieved_proposal.get('carouselCreatives', [])) == 2, "Carousel creatives count"),
                    (retrieved_proposal.get('expectedResults') == complete_data['expectedResults'], "Expected results"),
                    (retrieved_proposal.get('customNotes') == complete_data['customNotes'], "Custom notes"),
                    (retrieved_proposal.get('brandName') == "Zeri Solutions", "Zeri brand name"),
                    (retrieved_proposal.get('contactEmail') == "zeriagencia@gmail.com", "Zeri contact email")
                ]
                
                all_passed = all(check[0] for check in checks)
                details = f"Status: {response.status_code}, Retrieved: {get_response.status_code}, ID: {proposal_id}"
                
                if all_passed:
                    print_test_result("All template features work together", True, details)
                    return proposal_id
                else:
                    failed_checks = [check[1] for check in checks if not check[0]]
                    print_test_result("All template features work together", False, f"{details}, Failed: {', '.join(failed_checks)}")
                    return None
            else:
                print_test_result("All template features work together", False, f"Failed to retrieve proposal: {get_response.status_code}")
                return None
        else:
            print_test_result("All template features work together", False, f"Failed to create proposal: {response.status_code}")
            return None
            
    except Exception as e:
        print_test_result("All template features work together", False, f"Exception: {str(e)}")
        return None

def test_update_proposal_template_preservation(proposal_id):
    """Test 4: Update Proposal - Verify Template Doesn't Override"""
    print("🧪 TEST 4: Update Proposal - Verify Template Doesn't Override")
    
    if not proposal_id:
        print_test_result("Update proposal template preservation", False, "No proposal ID provided")
        return False
    
    try:
        # First, get the current proposal
        get_response = requests.get(f"{BASE_URL}/proposals/{proposal_id}", timeout=10)
        
        if get_response.status_code != 200:
            print_test_result("Update proposal template preservation", False, f"Failed to get proposal: {get_response.status_code}")
            return False
            
        original_proposal = get_response.json().get('proposal', {})
        
        # Update only the price of the first plan
        update_data = {
            "plans": [
                {
                    "name": original_proposal.get('plans', [{}])[0].get('name'),
                    "price": "R$ 5.000",  # Changed price
                    "features": original_proposal.get('plans', [{}])[0].get('features', [])
                }
            ]
        }
        
        # Update the proposal
        update_response = requests.put(f"{BASE_URL}/proposals/{proposal_id}", json=update_data, timeout=10)
        
        if update_response.status_code == 200:
            updated_proposal = update_response.json().get('proposal', {})
            
            # Verify only the updated field changes, template shouldn't reset other fields
            checks = [
                (updated_proposal.get('plans', [{}])[0].get('price') == "R$ 5.000", "Price updated correctly"),
                (updated_proposal.get('title') == original_proposal.get('title'), "Title preserved"),
                (updated_proposal.get('strategyOverview') == original_proposal.get('strategyOverview'), "Strategy overview preserved"),
                (updated_proposal.get('brandName') == original_proposal.get('brandName'), "Brand name preserved"),
                (updated_proposal.get('contactEmail') == original_proposal.get('contactEmail'), "Contact email preserved"),
                (updated_proposal.get('mainCreative') == original_proposal.get('mainCreative'), "Main creative preserved"),
                (len(updated_proposal.get('carouselCreatives', [])) == len(original_proposal.get('carouselCreatives', [])), "Carousel creatives preserved"),
                (updated_proposal.get('expectedResults') == original_proposal.get('expectedResults'), "Expected results preserved"),
                (updated_proposal.get('customNotes') == original_proposal.get('customNotes'), "Custom notes preserved")
            ]
            
            all_passed = all(check[0] for check in checks)
            details = f"Status: {update_response.status_code}, Updated price: {updated_proposal.get('plans', [{}])[0].get('price')}"
            
            if all_passed:
                print_test_result("Update proposal template preservation", True, details)
                return True
            else:
                failed_checks = [check[1] for check in checks if not check[0]]
                print_test_result("Update proposal template preservation", False, f"{details}, Failed: {', '.join(failed_checks)}")
                return False
        else:
            print_test_result("Update proposal template preservation", False, f"Update failed: {update_response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Update proposal template preservation", False, f"Exception: {str(e)}")
        return False

def test_crud_operations_with_template():
    """Test 5: Verify All CRUD Operations Work with Template System"""
    print("🧪 TEST 5: Verify All CRUD Operations Work with Template System")
    
    try:
        # Test data with template
        test_data = {
            "clientName": "Ana Costa",
            "companyName": "Moda & Estilo LTDA",
            "title": "Proposta de Gestão de Conteúdo para Mídias Digitais",
            "plans": [
                {
                    "name": "Plano Essencial",
                    "price": "R$ 2.800",
                    "features": ["Gestão do Instagram", "10 posts mensais"]
                }
            ],
            "brandName": "Zeri Solutions",
            "contactEmail": "zeriagencia@gmail.com"
        }
        
        # CREATE
        create_response = requests.post(f"{BASE_URL}/proposals", json=test_data, timeout=10)
        if create_response.status_code != 201:
            print_test_result("CRUD operations with template", False, f"CREATE failed: {create_response.status_code}")
            return False
            
        proposal_id = create_response.json().get('proposal', {}).get('id')
        
        # READ (single)
        read_response = requests.get(f"{BASE_URL}/proposals/{proposal_id}", timeout=10)
        if read_response.status_code != 200:
            print_test_result("CRUD operations with template", False, f"READ failed: {read_response.status_code}")
            return False
            
        # READ (all)
        read_all_response = requests.get(f"{BASE_URL}/proposals", timeout=10)
        if read_all_response.status_code != 200:
            print_test_result("CRUD operations with template", False, f"READ ALL failed: {read_all_response.status_code}")
            return False
            
        # UPDATE
        update_data = {"plans": [{"name": "Plano Essencial", "price": "R$ 3.100", "features": ["Gestão do Instagram", "12 posts mensais"]}]}
        update_response = requests.put(f"{BASE_URL}/proposals/{proposal_id}", json=update_data, timeout=10)
        if update_response.status_code != 200:
            print_test_result("CRUD operations with template", False, f"UPDATE failed: {update_response.status_code}")
            return False
            
        # Verify update preserved template data
        updated_proposal = update_response.json().get('proposal', {})
        template_preserved = (
            updated_proposal.get('title') == test_data['title'] and
            updated_proposal.get('brandName') == test_data['brandName'] and
            updated_proposal.get('plans', [{}])[0].get('price') == "R$ 3.100"
        )
        
        if not template_preserved:
            print_test_result("CRUD operations with template", False, "UPDATE didn't preserve template data")
            return False
            
        # DELETE
        delete_response = requests.delete(f"{BASE_URL}/proposals/{proposal_id}", timeout=10)
        if delete_response.status_code != 200:
            print_test_result("CRUD operations with template", False, f"DELETE failed: {delete_response.status_code}")
            return False
            
        # Verify deletion
        verify_delete_response = requests.get(f"{BASE_URL}/proposals/{proposal_id}", timeout=10)
        if verify_delete_response.status_code != 404:
            print_test_result("CRUD operations with template", False, f"DELETE verification failed: {verify_delete_response.status_code}")
            return False
            
        print_test_result("CRUD operations with template", True, "All CRUD operations working with template system")
        return True
        
    except Exception as e:
        print_test_result("CRUD operations with template", False, f"Exception: {str(e)}")
        return False

def main():
    """Run all template system tests"""
    print("=" * 80)
    print("🚀 PROPOSAL TEMPLATE SYSTEM TESTING")
    print("=" * 80)
    print(f"Testing against: {BASE_URL}")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Track test results
    results = []
    
    # Test 1: Create New Proposal with Template
    proposal_id_1 = test_create_proposal_with_template()
    results.append(("Create proposal with template", proposal_id_1 is not None))
    
    # Test 2: Create Proposal with Custom Prices
    proposal_id_2 = test_create_proposal_with_custom_prices()
    results.append(("Create proposal with custom prices", proposal_id_2 is not None))
    
    # Test 3: Verify All Template Features Work Together
    proposal_id_3 = test_all_template_features_together()
    results.append(("All template features work together", proposal_id_3 is not None))
    
    # Test 4: Update Proposal - Verify Template Doesn't Override
    update_success = test_update_proposal_template_preservation(proposal_id_3)
    results.append(("Update proposal template preservation", update_success))
    
    # Test 5: Verify All CRUD Operations Work with Template System
    crud_success = test_crud_operations_with_template()
    results.append(("CRUD operations with template", crud_success))
    
    # Summary
    print("=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TEMPLATE SYSTEM TESTS PASSED!")
        return 0
    else:
        print("⚠️  SOME TEMPLATE SYSTEM TESTS FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())