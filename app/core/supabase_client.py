from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv() 

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY or not SUPABASE_SERVICE_KEY:
    raise ValueError("Supabase URL or keys are not set in environment variables")


# Client read-only
supabase_anon = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Client full quyền
supabase_service = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)