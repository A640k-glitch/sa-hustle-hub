# GitHub Pages Deployment Guide

## Prerequisites
- A GitHub account (free).
- Git installed on your PC.

## Steps

### 1. Create the GitHub Repository
1. Go to [github.com/new](https://github.com/new).
2. Name it: `sa-hustle-hub` (or your preferred name).
3. Set visibility to **Public** (required for free GitHub Pages).
4. Click **Create repository**.

### 2. Push Your Code
Open PowerShell in `C:\Users\Acer\.gemini\antigravity\scratch\blast_system` and run:

```powershell
git init
git add .
git commit -m "Initial deploy: SA Hustle Hub"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/sa-hustle-hub.git
git push -u origin main
```

### 3. Enable GitHub Pages
1. Go to your repo on GitHub → **Settings** → **Pages**.
2. Under **Source**, select **Deploy from a branch**.
3. Set branch to `main`, folder to `/public`.
4. Click **Save**.

Your site will go live at:
`https://YOUR_USERNAME.github.io/sa-hustle-hub/`

(Takes ~2 minutes the first time.)

### 4. Updating the Site
After adding new content articles, rebuild and push:

```powershell
py tools/build_blog.py
git add public/
git commit -m "Add new hustle: [article name]"
git push
```

GitHub Pages will auto-deploy within ~60 seconds.
