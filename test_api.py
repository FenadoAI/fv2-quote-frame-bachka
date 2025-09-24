#!/usr/bin/env python3
"""
Test script for the Quote Generator API
"""

import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_root():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print("Root endpoint:", response.json())
    return response.status_code == 200

def test_people():
    """Test people endpoint"""
    response = requests.get(f"{BASE_URL}/people")
    print(f"People endpoint: {len(response.json())} people found")
    return response.status_code == 200

def test_quotes():
    """Test quotes endpoint"""
    response = requests.get(f"{BASE_URL}/quotes")
    quotes = response.json()
    print(f"Quotes endpoint: {len(quotes)} quotes found")
    if quotes:
        print(f"Sample quote: {quotes[0]}")
    return response.status_code == 200

def test_random_quote():
    """Test random quote endpoint"""
    response = requests.get(f"{BASE_URL}/quotes/random")
    if response.status_code == 200:
        quote = response.json()
        print(f"Random quote: '{quote['text']}' - {quote['person_name']}")
        return True
    else:
        print("Random quote failed:", response.text)
        return False

def test_quotes_by_person():
    """Test quotes by person endpoint"""
    # First get a person
    people_response = requests.get(f"{BASE_URL}/people")
    if people_response.status_code != 200 or not people_response.json():
        print("No people found for person quotes test")
        return False

    person = people_response.json()[0]
    response = requests.get(f"{BASE_URL}/quotes/person/{person['id']}")
    if response.status_code == 200:
        quotes = response.json()
        print(f"Quotes by {person['name']}: {len(quotes)} found")
        return True
    else:
        print("Quotes by person failed:", response.text)
        return False

def main():
    print("Testing Quote Generator API...\n")

    tests = [
        ("Root endpoint", test_root),
        ("People endpoint", test_people),
        ("Quotes endpoint", test_quotes),
        ("Random quote endpoint", test_random_quote),
        ("Quotes by person endpoint", test_quotes_by_person),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"✅ {test_name}: {'PASSED' if result else 'FAILED'}\n")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}\n")
            results.append((test_name, False))

    # Summary
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTest Summary: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed")

if __name__ == "__main__":
    main()