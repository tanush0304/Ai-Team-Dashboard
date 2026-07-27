import os
import httpx
from supabase import create_client, Client

# Retrieve credentials from .env
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

# Initialize client cleanly without extra options
supabase: Client = create_client(url, key)

# Force HTTP/1.1 session on postgrest to fix Windows socket read issues
http_client = httpx.Client(http2=False)
supabase.postgrest.session = http_client