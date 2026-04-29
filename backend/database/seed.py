import asyncio
import motor.motor_asyncio
from models import Product

# Product data to seed
products = [
    {
        "name": "Silicone Teether Set",
        "price": 45.0,
        "currency": "AED",
        "category": "teething",
        "age_min": 3,
        "age_max": 12,
        "rating": 4.8,
        "review_count": 150,
        "tags": ["safe", "bpa-free", "giftable", "soft"],
        "description": "Safe and soft silicone teething toys for babies. Easy to grip and clean.",
        "in_stock": True
    },
    {
        "name": "Organic Cotton Baby Onesie",
        "price": 85.0,
        "currency": "AED",
        "category": "clothing",
        "age_min": 0,
        "age_max": 24,
        "rating": 4.5,
        "review_count": 80,
        "tags": ["organic", "comfortable", "clothing"],
        "description": "Ultra-soft organic cotton onesies for everyday comfort.",
        "in_stock": True
    },
    {
        "name": "Musical Activity Cube",
        "price": 120.0,
        "currency": "AED",
        "category": "toys",
        "age_min": 6,
        "age_max": 36,
        "rating": 4.7,
        "review_count": 210,
        "tags": ["educational", "musical", "interactive"],
        "description": "Multi-functional activity cube with music, lights, and learning games.",
        "in_stock": True
    },
    {
        "name": "Soft Plush Elephant",
        "price": 60.0,
        "currency": "AED",
        "category": "toys",
        "age_min": 0,
        "age_max": 60,
        "rating": 4.9,
        "review_count": 300,
        "tags": ["plush", "soft", "gift"],
        "description": "Adorable and cuddly plush elephant for babies and toddlers.",
        "in_stock": True
    },
    {
        "name": "Stacking Rings Toy",
        "price": 35.0,
        "currency": "AED",
        "category": "toys",
        "age_min": 6,
        "age_max": 24,
        "rating": 4.6,
        "review_count": 120,
        "tags": ["classic", "developmental", "colorful"],
        "description": "Classic stacking rings toy to help develop fine motor skills.",
        "in_stock": True
    },
    {
        "name": "Baby Milestone Blanket",
        "price": 95.0,
        "currency": "AED",
        "category": "decor",
        "age_min": 0,
        "age_max": 12,
        "rating": 4.7,
        "review_count": 55,
        "tags": ["giftable", "photography", "keepsake"],
        "description": "Beautiful blanket to capture monthly growth milestones of your baby.",
        "in_stock": True
    },
    {
        "name": "High Contrast Flash Cards",
        "price": 25.0,
        "currency": "AED",
        "category": "educational",
        "age_min": 0,
        "age_max": 6,
        "rating": 4.8,
        "review_count": 90,
        "tags": ["sensory", "visual-development", "educational"],
        "description": "Black and white high-contrast cards for newborn visual stimulation.",
        "in_stock": True
    },
    {
        "name": "Wooden Shape Sorter",
        "price": 75.0,
        "currency": "AED",
        "category": "toys",
        "age_min": 12,
        "age_max": 48,
        "rating": 4.4,
        "review_count": 140,
        "tags": ["wooden", "montessori", "educational"],
        "description": "Durable wooden shape sorter to teach shapes and colors.",
        "in_stock": True
    },
    {
        "name": "Interactive Baby Walker",
        "price": 180.0,
        "currency": "AED",
        "category": "gear",
        "age_min": 9,
        "age_max": 36,
        "rating": 4.6,
        "review_count": 450,
        "tags": ["mobility", "interactive", "walking-aid"],
        "description": "Sturdy walker with interactive panel to help baby take their first steps.",
        "in_stock": True
    },
    {
        "name": "Silicone Feeding Set",
        "price": 110.0,
        "currency": "AED",
        "category": "feeding",
        "age_min": 6,
        "age_max": 36,
        "rating": 4.7,
        "review_count": 180,
        "tags": ["self-feeding", "bpa-free", "suction-base"],
        "description": "Complete silicone bowl, plate, and spoon set for weaning babies.",
        "in_stock": True
    },
    {
        "name": "Bath Toy Organizer",
        "price": 40.0,
        "currency": "AED",
        "category": "bath",
        "age_min": 0,
        "age_max": 72,
        "rating": 4.3,
        "review_count": 65,
        "tags": ["storage", "practical", "bath-time"],
        "description": "Mesh bag for easy storage and drying of bath toys.",
        "in_stock": True
    },
    {
        "name": "Sensory Ball Set",
        "price": 55.0,
        "currency": "AED",
        "category": "toys",
        "age_min": 0,
        "age_max": 36,
        "rating": 4.5,
        "review_count": 110,
        "tags": ["sensory", "textured", "developmental"],
        "description": "Set of 6 uniquely textured balls for sensory exploration.",
        "in_stock": True
    },
    {
        "name": "Personalized Story Book",
        "price": 150.0,
        "currency": "AED",
        "category": "books",
        "age_min": 12,
        "age_max": 84,
        "rating": 4.9,
        "review_count": 200,
        "tags": ["personalized", "gift", "educational"],
        "description": "A magical story book featuring your child's name and character.",
        "in_stock": True
    },
    {
        "name": "Infant Swaddle Wrap",
        "price": 70.0,
        "currency": "AED",
        "category": "bedding",
        "age_min": 0,
        "age_max": 4,
        "rating": 4.6,
        "review_count": 95,
        "tags": ["sleep", "comfort", "safe-sleep"],
        "description": "Easy-to-use swaddle wrap for a peaceful night's sleep.",
        "in_stock": True
    },
    {
        "name": "Baby Grooming Kit",
        "price": 65.0,
        "currency": "AED",
        "category": "health",
        "age_min": 0,
        "age_max": 48,
        "rating": 4.2,
        "review_count": 130,
        "tags": ["essential", "health", "grooming"],
        "description": "Complete grooming set including brush, comb, and nail clippers.",
        "in_stock": True
    }
]

async def seed_db():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["mama_db"]
    collection = db["products"]
    
    # Clear existing data
    await collection.delete_many({})
    
    # Insert new data
    result = await collection.insert_many(products)
    print(f"Seeded {len(result.inserted_ids)} products.")

if __name__ == "__main__":
    asyncio.run(seed_db())
