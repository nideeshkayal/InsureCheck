def get_claim_data(claim_id):

    if claim_id is None:
        return {
            'success': False,
            'error': 'claim_id is required. Please provide a valid claim ID.'
        }
    
    sample_claims = {
        1: {
            'claim_id': 1,
            'date_of_service': '2024-09-12',
            'received_date': '2024-09-15',
            'added_by': 'Dr. Mehta Clinic',
            
            'status': {
                'status_id': 1,
                'claim_status': 'Approved',
                'status_type': 'Final'
            },
            
            'member': {
                'member_id': 1001,
                'first_name': 'Shiwani',
                'last_name': 'Gupta',
                'full_name': 'Shiwani Gupta',
                'gender': 'Female',
                'date_of_birth': '1992-06-18',
                'policy_id': 1
            },
            
            'address': {
                'address_id': 501,
                'street_address': '12/B Linking Road',
                'apartment_no': 304,
                'city': 'Mumbai',
                'county': 'Mumbai Suburban',
                'country': 'India',
                'zipcode': '400050'
            },
            
            'coverage': {
                'coverage_id': 2001,
                'coverage_name': 'Family Floater - Gold',
                'effective_date': '2024-04-01',
                'term_date': '2025-03-31'
            },
            
            'payment': {
                'claim_payment_id': 3001,
                'billed_amount': '45000',
                'approved_amount': '38000',
                'copay_amount': '2000',
                'coinsurance_amount': '3800',
                'deductible_amount': '5000',
                'net_payment': '27200'
            }
        },
        2: {
            'claim_id': 2,
            'date_of_service': '2024-10-05',
            'received_date': '2024-10-08',
            'added_by': 'Fortis Hospital',
            
            'status': {
                'status_id': 2,
                'claim_status': 'Pending Review',
                'status_type': 'In Progress'
            },
            
            'member': {
                'member_id': 1002,
                'first_name': 'Nideesh',
                'last_name': 'Kayal',
                'full_name': 'Nideesh Kayal',
                'gender': 'Male',
                'date_of_birth': '1988-11-24',
                'policy_id': 2
            },
            
            'address': {
                'address_id': 502,
                'street_address': '45 MG Road',
                'apartment_no': 1502,
                'city': 'Bangalore',
                'county': 'Bangalore Urban',
                'country': 'India',
                'zipcode': '560001'
            },
            
            'coverage': {
                'coverage_id': 2002,
                'coverage_name': 'Individual Health - Premium',
                'effective_date': '2024-01-15',
                'term_date': '2025-01-14'
            },
            
            'payment': {
                'claim_payment_id': 3002,
                'billed_amount': '125000',
                'approved_amount': '95000',
                'copay_amount': '5000',
                'coinsurance_amount': '9500',
                'deductible_amount': '10000',
                'net_payment': '70500'
            }
        },
        3: {
            'claim_id': 3,
            'date_of_service': '2024-08-22',
            'received_date': '2024-08-25',
            'added_by': 'Apollo Pharmacy',
            
            'status': {
                'status_id': 3,
                'claim_status': 'Denied',
                'status_type': 'Final'
            },
            
            'member': {
                'member_id': 1003,
                'first_name': 'Yohaan',
                'last_name': 'Khan',
                'full_name': 'Yohaan Khan',
                'gender': 'Male',
                'date_of_birth': '1995-02-07',
                'policy_id': 3
            },
            
            'address': {
                'address_id': 503,
                'street_address': '78 Civil Lines',
                'apartment_no': 202,
                'city': 'Delhi',
                'county': 'New Delhi',
                'country': 'India',
                'zipcode': '110054'
            },
            
            'coverage': {
                'coverage_id': 2003,
                'coverage_name': 'Basic Health Cover',
                'effective_date': '2024-06-01',
                'term_date': '2025-05-31'
            },
            
            'payment': {
                'claim_payment_id': 3003,
                'billed_amount': '8500',
                'approved_amount': '0',
                'copay_amount': '0',
                'coinsurance_amount': '0',
                'deductible_amount': '0',
                'net_payment': '0'
            }
        },
        4: {
            'claim_id': 4,
            'date_of_service': '2024-10-18',
            'received_date': '2024-10-20',
            'added_by': 'Manipal Hospital',
            
            'status': {
                'status_id': 4,
                'claim_status': 'Under Investigation',
                'status_type': 'In Progress'
            },
            
            'member': {
                'member_id': 1004,
                'first_name': 'Raghav',
                'last_name': 'Bhati',
                'full_name': 'Raghav Bhati',
                'gender': 'Male',
                'date_of_birth': '1985-09-30',
                'policy_id': 4
            },
            
            'address': {
                'address_id': 504,
                'street_address': '23 Koregaon Park',
                'apartment_no': 801,
                'city': 'Pune',
                'county': 'Pune',
                'country': 'India',
                'zipcode': '411001'
            },
            
            'coverage': {
                'coverage_id': 2004,
                'coverage_name': 'Family Floater - Platinum',
                'effective_date': '2024-03-10',
                'term_date': '2025-03-09'
            },
            
            'payment': {
                'claim_payment_id': 3004,
                'billed_amount': '285000',
                'approved_amount': '240000',
                'copay_amount': '15000',
                'coinsurance_amount': '24000',
                'deductible_amount': '20000',
                'net_payment': '181000'
            }
        },
        5: {
            'claim_id': 5,
            'date_of_service': '2024-09-28',
            'received_date': '2024-09-30',
            'added_by': 'Max Healthcare',
            
            'status': {
                'status_id': 5,
                'claim_status': 'Paid',
                'status_type': 'Final'
            },
            
            'member': {
                'member_id': 1005,
                'first_name': 'Lily',
                'last_name': 'Shetty',
                'full_name': 'Lily Shetty',
                'gender': 'Female',
                'date_of_birth': '1990-04-15',
                'policy_id': 5
            },
            
            'address': {
                'address_id': 505,
                'street_address': '156 Residency Road',
                'apartment_no': 603,
                'city': 'Bangalore',
                'county': 'Bangalore Urban',
                'country': 'India',
                'zipcode': '560025'
            },
            
            'coverage': {
                'coverage_id': 2005,
                'coverage_name': 'Individual Health - Standard',
                'effective_date': '2024-02-20',
                'term_date': '2025-02-19'
            },
            
            'payment': {
                'claim_payment_id': 3005,
                'billed_amount': '62000',
                'approved_amount': '55000',
                'copay_amount': '3000',
                'coinsurance_amount': '5500',
                'deductible_amount': '7000',
                'net_payment': '39500'
            }
        }
    }
    
    if claim_id not in sample_claims:
        return {
            'success': False,
            'error': f'Claim ID {claim_id} not found in database.'
        }
    
    return {
        'success': True,
        'data': sample_claims[claim_id]
    }