#!/usr/bin/env python3
"""
Quick Deployment Script - Provides step-by-step deployment instructions
"""

import os
import subprocess
import sys

def check_git_status():
    """Check if git repository is ready for deployment."""
    print("🔍 CHECKING GIT STATUS")
    print("=" * 40)
    
    try:
        # Check if git is initialized
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository: READY")
            
            # Check for uncommitted changes
            if "nothing to commit" in result.stdout:
                print("✅ All changes committed")
            else:
                print("⚠️  Uncommitted changes detected")
                print("   Run: git add . && git commit -m 'Ready for deployment'")
                return False
        else:
            print("❌ Git not initialized")
            print("   Run: git init && git add . && git commit -m 'Initial commit'")
            return False
            
    except FileNotFoundError:
        print("❌ Git not installed")
        print("   Please install Git first")
        return False
    
    return True

def check_files():
    """Check if all required files are present."""
    print("\n📁 CHECKING REQUIRED FILES")
    print("=" * 40)
    
    required_files = [
        'hackrx_api.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'app.py'
    ]
    
    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            all_present = False
    
    return all_present

def show_deployment_options():
    """Show deployment options."""
    print("\n🚀 DEPLOYMENT OPTIONS")
    print("=" * 40)
    
    print("1. 🎯 RENDER (Recommended - Free)")
    print("   - Go to: https://render.com")
    print("   - Sign up/Login")
    print("   - Click 'New +' → 'Web Service'")
    print("   - Connect your GitHub repository")
    print("   - Configure:")
    print("     • Name: hackrx-llm-api")
    print("     • Environment: Python 3")
    print("     • Build Command: pip install -r requirements.txt")
    print("     • Start Command: gunicorn hackrx_api:app")
    print("     • Plan: Free")
    
    print("\n2. 🚄 RAILWAY (Recommended - Free)")
    print("   - Go to: https://railway.app")
    print("   - Sign up/Login with GitHub")
    print("   - Click 'New Project' → 'Deploy from GitHub repo'")
    print("   - Select your repository")
    print("   - Railway will auto-detect and deploy")
    
    print("\n3. 🌐 VERCEL (Serverless)")
    print("   - Go to: https://vercel.com")
    print("   - Import your GitHub repository")
    print("   - Configure as Python project")
    print("   - Deploy")
    
    print("\n4. ⚡ HEROKU (Paid)")
    print("   - Install Heroku CLI")
    print("   - Run: heroku create hackrx-llm-api")
    print("   - Run: git push heroku main")

def show_test_instructions():
    """Show testing instructions."""
    print("\n🧪 TESTING INSTRUCTIONS")
    print("=" * 40)
    
    print("After deployment, test your API:")
    print()
    print("1. Test Health Endpoint:")
    print("   curl https://your-app-name.onrender.com/api/v1/health")
    print()
    print("2. Test Main Endpoint:")
    print("   curl -X POST https://your-app-name.onrender.com/api/v1/hackrx/run \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -H 'Authorization: Bearer 8b796ad826037b97ba28ae4cd36c4605bd9ed1464673ad5b0a3290a9867a9d21' \\")
    print("     -d '{")
    print('       "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",')
    print('       "questions": ["What is the grace period for premium payment?"]')
    print("     }'")
    print()
    print("3. Update deploy_test.py with your URL and run:")
    print("   python deploy_test.py")

def show_submission_instructions():
    """Show submission instructions."""
    print("\n🎯 HACKRX SUBMISSION")
    print("=" * 40)
    
    print("Once deployed and tested:")
    print()
    print("1. Go to HackRx competition page")
    print("2. Click 'Submit'")
    print("3. Enter your webhook URL:")
    print("   https://your-app-name.onrender.com/api/v1/hackrx/run")
    print("4. Add description:")
    print("   Flask + FAISS + Sentence Transformers + LLM")
    print("5. Click 'Run' to test")
    print("6. Submit if all tests pass!")

def main():
    """Main deployment guide."""
    print("🚀 HACKRX LLM API - QUICK DEPLOYMENT GUIDE")
    print("=" * 60)
    
    # Check prerequisites
    git_ready = check_git_status()
    files_ready = check_files()
    
    if not git_ready or not files_ready:
        print("\n❌ Please fix the issues above before deploying")
        return
    
    print("\n✅ ALL PREREQUISITES MET - READY FOR DEPLOYMENT!")
    
    # Show deployment options
    show_deployment_options()
    
    # Show testing instructions
    show_test_instructions()
    
    # Show submission instructions
    show_submission_instructions()
    
    print("\n" + "=" * 60)
    print("🎯 YOUR SYSTEM IS READY FOR DEPLOYMENT!")
    print("=" * 60)
    print("\nChoose a deployment option above and follow the steps.")
    print("After deployment, test your API and submit to HackRx!")

if __name__ == "__main__":
    main() 