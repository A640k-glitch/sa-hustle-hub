# Project Constitution

## 1. Data Schemas

### Input: Content Markdown (.md) Frontmatter
```json
{
  "title": "String",
  "description": "String",
  "category": "String (e.g., Remote, Apps, Locally-Based)",
  "difficulty": "String (Easy, Moderate, High)",
  "data_usage": "String (Low, Medium, High)",
  "verified_date": "ISO-8601",
  "link": "URL",
  "tags": ["String"]
}
```

### Output: Search Index (index.json)
```json
[
  {
    "slug": "String",
    "title": "String",
    "description": "String",
    "category": "String",
    "tags": ["String"]
  }
]
```

## 2. Behavioral Rules
- **Tone**: Street-smart, empathetic, resourceful (South African context).
- **Data-Lite**: Page size < 100KB. No external fonts/heavy JS.
- **Verification**: Only zero-capital, non-betting opportunities.

## 3. Architectural Invariants
- **Source of Truth**: Plain Markdown in `/content`.
- **Engine**: Periodic Python-based rebuild to `/public`.
- **Search**: Client-side filtering of `index.json`.
