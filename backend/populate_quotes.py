#!/usr/bin/env python3
"""
Script to populate the quotes database with famous people and their quotes
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Famous people and quotes data
FAMOUS_PEOPLE_QUOTES = [
    {
        "name": "Albert Einstein",
        "description": "Theoretical physicist known for the theory of relativity",
        "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&h=500&fit=crop&crop=face",
        "quotes": [
            "Imagination is more important than knowledge.",
            "Try not to become a person of success, but rather try to become a person of value.",
            "Life is like riding a bicycle. To keep your balance, you must keep moving.",
            "The important thing is not to stop questioning.",
            "Anyone who has never made a mistake has never tried anything new."
        ]
    },
    {
        "name": "Maya Angelou",
        "description": "American poet, memoirist, and civil rights activist",
        "image_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=500&h=500&fit=crop&crop=face",
        "quotes": [
            "If you don't like something, change it. If you can't change it, change your attitude.",
            "I've learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.",
            "There is no greater agony than bearing an untold story inside you.",
            "We delight in the beauty of the butterfly, but rarely admit the changes it has gone through to achieve that beauty.",
            "Success is liking yourself, liking what you do, and liking how you do it."
        ]
    },
    {
        "name": "Steve Jobs",
        "description": "Co-founder and CEO of Apple Inc.",
        "image_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=500&h=500&fit=crop&crop=face",
        "quotes": [
            "Innovation distinguishes between a leader and a follower.",
            "Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work.",
            "Stay hungry, stay foolish.",
            "Design is not just what it looks like and feels like. Design is how it works.",
            "The only way to do great work is to love what you do."
        ]
    },
    {
        "name": "Winston Churchill",
        "description": "British statesman and Prime Minister during WWII",
        "image_url": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=500&h=500&fit=crop&crop=face",
        "quotes": [
            "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "We make a living by what we get, but we make a life by what we give.",
            "The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.",
            "Courage is what it takes to stand up and speak; courage is also what it takes to sit down and listen.",
            "Never give in, never give in, never, never, never, never."
        ]
    },
    {
        "name": "Oprah Winfrey",
        "description": "Media executive, actress, and philanthropist",
        "image_url": "https://images.unsplash.com/photo-1594736797933-d0f6ed0e1ee1?w=500&h=500&fit=crop&crop=face",
        "quotes": [
            "The biggest adventure you can take is to live the life of your dreams.",
            "Be thankful for what you have; you'll end up having more.",
            "You become what you believe.",
            "The greatest discovery of all time is that a person can change his future by merely changing his attitude.",
            "Turn your wounds into wisdom."
        ]
    },
    {
        "name": "Martin Luther King Jr.",
        "description": "Civil rights leader and activist",
        "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&h=500&fit=crop&crop=face",
        "quotes": [
            "Darkness cannot drive out darkness; only light can do that. Hate cannot drive out hate; only love can do that.",
            "The ultimate measure of a man is not where he stands in moments of comfort and convenience, but where he stands at times of challenge and controversy.",
            "Injustice anywhere is a threat to justice everywhere.",
            "Faith is taking the first step even when you don't see the whole staircase.",
            "Life's most persistent and urgent question is: What are you doing for others?"
        ]
    },
    {
        "name": "Mark Twain",
        "description": "American writer, humorist, and lecturer",
        "image_url": "https://images.unsplash.com/photo-1531427186611-ecfd6d936c79?w=500&h=500&fit=crop&crop=face",
        "quotes": [
            "The two most important days in your life are the day you are born and the day you find out why.",
            "Kindness is the language which the deaf can hear and the blind can see.",
            "Courage is resistance to fear, mastery of fear, not absence of fear.",
            "Always do right. This will gratify some people and astonish the rest.",
            "Don't go around saying the world owes you a living. The world owes you nothing. It was here first."
        ]
    },
    {
        "name": "Nelson Mandela",
        "description": "South African anti-apartheid revolutionary and President",
        "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&h=500&fit=crop&crop=face",
        "quotes": [
            "Education is the most powerful weapon which you can use to change the world.",
            "It always seems impossible until it's done.",
            "I learned that courage was not the absence of fear, but the triumph over it.",
            "A good head and good heart are always a formidable combination.",
            "There is no passion to be found playing small – in settling for a life that is less than the one you are capable of living."
        ]
    }
]

async def populate_database():
    """Populate the database with famous people and their quotes"""
    print("Starting database population...")

    # Clear existing data
    await db.people.delete_many({})
    await db.quotes.delete_many({})
    print("Cleared existing data")

    total_people = 0
    total_quotes = 0

    for person_data in FAMOUS_PEOPLE_QUOTES:
        # Create person
        person = {
            "id": str(uuid.uuid4()),
            "name": person_data["name"],
            "description": person_data["description"],
            "image_url": person_data["image_url"],
            "created_at": datetime.utcnow()
        }

        await db.people.insert_one(person)
        total_people += 1
        print(f"Added person: {person['name']}")

        # Create quotes for this person
        for quote_text in person_data["quotes"]:
            quote = {
                "id": str(uuid.uuid4()),
                "person_id": person["id"],
                "text": quote_text,
                "created_at": datetime.utcnow()
            }

            await db.quotes.insert_one(quote)
            total_quotes += 1

        print(f"  Added {len(person_data['quotes'])} quotes")

    print(f"\nDatabase population complete!")
    print(f"Total people added: {total_people}")
    print(f"Total quotes added: {total_quotes}")

async def main():
    try:
        await populate_database()
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())