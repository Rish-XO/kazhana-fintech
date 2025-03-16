from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")

# Ensure it uses `asyncpg`
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

if not DATABASE_URL:
    raise ValueError("❌ ERROR: SUPABASE_DATABASE_URL is missing or incorrect!")

# Create Async Database Engine
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependency to get database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
