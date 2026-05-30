#!/bin/bash

# Color styles for professional logging
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}================================================================${NC}"
echo -e "${CYAN}     🛡️  SILENTGUARD AI 2.0 - AUTOMATED REPO REBUILD & PUSH  🛡️     ${NC}"
echo -e "${CYAN}================================================================${NC}"

# Navigate to the exact project folder to avoid parent Git conflicts
cd "/Users/vekariadharmeshh/Downloads/AI-Spyware-Detection-System-main" || exit 1

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}[ERROR] Git is not installed or not in PATH.${NC}"
    exit 1
fi

# 1. Initialize local Git specifically inside the project folder
if [ ! -d ".git" ]; then
    echo -e "${CYAN}[1/5] Initializing new Git repository in project folder...${NC}"
    git init
else
    echo -e "${CYAN}[1/5] Found existing local Git. Refreshing configurations...${NC}"
fi

# 2. Rename default branch to main
git branch -M main

# 3. Add/Reset remote origin link to your GitHub repository
echo -e "${CYAN}[2/5] Binding remote origin to VekariaDharmesh/AI-Spyware-Detection-System...${NC}"
git remote remove origin 2>/dev/null
git remote add origin https://github.com/VekariaDharmesh/AI-Spyware-Detection-System.git

# 4. Stage and commit only local project files
echo -e "${CYAN}[3/5] Staging files...${NC}"
git add .

echo -e "${CYAN}[4/5] Committing changes...${NC}"
git commit -m "feat: complete modern SaaS UI/UX redesign and FastAPI REST backend engine"

# 5. Push and bind upstream
echo -e "${CYAN}[5/5] Force-pushing package to remote GitHub repository...${NC}"
echo -e "${CYAN}Note: If prompted, please enter your GitHub username and Personal Access Token (PAT).${NC}"

if git push -u origin main --force; then
    echo -e "${GREEN}================================================================${NC}"
    echo -e "${GREEN}🎉 SUCCESS! Your GitHub repository is completely up to date!${NC}"
    echo -e "${GREEN}================================================================${NC}"
else
    echo -e "${RED}================================================================${NC}"
    echo -e "${RED}❌ PUSH FAILED. Please check if you need to enter a GitHub Personal Access Token (PAT).${NC}"
    echo -e "${RED}================================================================${NC}"
    exit 1
fi
