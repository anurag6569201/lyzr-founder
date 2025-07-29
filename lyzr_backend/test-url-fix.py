# TEST SCRIPT - Validate URL Endpoint Fix

"""
Quick test script to validate that the URL knowledge source indexing is now working.
Run this after deploying the fixed LyzrClient to test the endpoint change.
"""

import os
import sys
import django
from django.conf import settings

# Add your Django project to the path
sys.path.append('/path/to/your/django/project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lyzr_backend.settings')
django.setup()

from core.services.lyzr_client import LyzrClient, LyzrAPIError
from core.models import KnowledgeSource, Agent
from core.tasks import index_knowledge_source_task

def test_url_endpoint():
    """Test the URL endpoint fix."""
    
    print("🔧 Testing Lyzr URL Endpoint Fix...")
    
    # Test 1: Direct API call
    print("\n1️⃣ Testing direct API call...")
    try:
        client = LyzrClient()
        
        # Use a test RAG ID (you'll need to replace with a real one)
        test_rag_id = "your_actual_rag_id_here"  # Replace with actual RAG ID
        test_url = "https://example.com"
        
        result = client.index_url(test_rag_id, test_url)
        print(f"✅ SUCCESS: URL endpoint working! Response: {result}")
        
    except LyzrAPIError as e:
        if e.status_code == 404:
            print(f"❌ STILL 404: {e.message}")
            print("   Check if you're using the correct endpoint: v3/train/website/")
        else:
            print(f"⚠️  Other error: {e.message}")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
    
    # Test 2: Test with actual knowledge source
    print("\n2️⃣ Testing with existing failed URL knowledge source...")
    try:
        # Find a failed URL knowledge source
        failed_url_source = KnowledgeSource.objects.filter(
            type='URL',
            status=KnowledgeSource.IndexingStatus.FAILED
        ).first()
        
        if failed_url_source:
            print(f"Found failed URL source: {failed_url_source.id}")
            print(f"URL: {failed_url_source.content}")
            
            # Retry indexing
            print("Retrying indexing...")
            index_knowledge_source_task.delay(failed_url_source.id)
            print("✅ Task queued. Check Celery logs for results.")
        else:
            print("No failed URL sources found to test with.")
            
    except Exception as e:
        print(f"💥 Error testing with knowledge source: {e}")
    
    # Test 3: Connection test
    print("\n3️⃣ Testing API connection...")
    try:
        client = LyzrClient()
        health = client.test_connection()
        print(f"Connection status: {health}")
    except Exception as e:
        print(f"💥 Connection test failed: {e}")

def verify_endpoint_usage():
    """Verify that your code is using the correct endpoint."""
    
    print("\n🔍 Verifying endpoint usage in your code...")
    
    # Check the LyzrClient index_url method
    try:
        client = LyzrClient()
        
        # This will show what endpoint is being used
        test_rag_id = "test_id"
        expected_endpoint = f"v3/train/website/?rag_id={test_rag_id}"
        
        print(f"Expected endpoint: {expected_endpoint}")
        print("✅ If your LyzrClient.index_url() method constructs this endpoint, you're good!")
        
    except Exception as e:
        print(f"Error during verification: {e}")

def quick_fix_guide():
    """Print a quick fix guide for common issues."""
    
    print("\n📋 QUICK FIX GUIDE:")
    print("=" * 50)
    print("1. Replace your core/services/lyzr_client.py with the fixed version")
    print("2. Replace your core/tasks.py with the fixed version")
    print("3. Restart Celery workers: pkill -f celery && celery -A lyzr_backend worker -l info &")
    print("4. Test with a new URL knowledge source")
    print("")
    print("Expected behavior:")
    print("✅ POST to https://rag-prod.studio.lyzr.ai/v3/train/website/?rag_id=<id>")
    print("❌ NOT to https://rag-prod.studio.lyzr.ai/v3/train/web/?rag_id=<id>")
    print("")
    print("If still getting 404:")
    print("- Check your LYZR_RAG_API_BASE_URL setting")
    print("- Verify your API key is correct")  
    print("- Ensure URL starts with http:// or https://")

if __name__ == "__main__":
    print("🚀 LYZR URL ENDPOINT FIX VALIDATOR")
    print("=" * 40)
    
    quick_fix_guide()
    test_url_endpoint()
    verify_endpoint_usage()
    
    print("\n✨ Test completed!")
    print("If you see ✅ SUCCESS messages, your fix is working!")
    print("If you see ❌ errors, check the fix guide above.")