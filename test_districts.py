#!/usr/bin/env python3
"""
Test script to verify state-district mapping functionality
"""

from config import STATE_DISTRICT_MAPPING
from data_generator import DataGenerator

def test_state_district_mapping():
    """Test the state-district mapping"""
    print("🌾 Testing State-District Mapping")
    print("=" * 50)
    
    # Test the mapping
    for state, districts in STATE_DISTRICT_MAPPING.items():
        print(f"\n📍 {state}:")
        for i, district in enumerate(districts, 1):
            print(f"   {i}. {district}")
    
    print(f"\n✅ Total States: {len(STATE_DISTRICT_MAPPING)}")
    print(f"✅ Total Districts: {sum(len(districts) for districts in STATE_DISTRICT_MAPPING.values())}")
    
    # Test data generation
    print("\n🧪 Testing Data Generation")
    print("=" * 50)
    
    generator = DataGenerator()
    yield_data = generator.generate_yield_data()
    
    print(f"✅ Generated {len(yield_data)} yield records")
    
    # Check state-district consistency
    print("\n🔍 Checking State-District Consistency")
    print("=" * 50)
    
    inconsistencies = []
    for _, row in yield_data.iterrows():
        state = row['state']
        district = row['district']
        if state in STATE_DISTRICT_MAPPING:
            if district not in STATE_DISTRICT_MAPPING[state]:
                inconsistencies.append(f"State: {state}, District: {district}")
    
    if inconsistencies:
        print("❌ Found inconsistencies:")
        for inc in inconsistencies[:10]:  # Show first 10
            print(f"   {inc}")
    else:
        print("✅ All state-district combinations are valid!")
    
    # Show sample data
    print("\n📊 Sample Generated Data")
    print("=" * 50)
    print(yield_data[['state', 'district', 'crop', 'season']].head(10).to_string(index=False))

if __name__ == "__main__":
    test_state_district_mapping()
