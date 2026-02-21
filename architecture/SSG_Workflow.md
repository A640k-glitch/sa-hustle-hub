# SSG Workflow SOP

## Goal
To convert Markdown content into a minified, data-efficient static website.

## Inputs
- Files in `/content/*.md`
- Templates in `/templates/*.html`

## Tools
- `tools/build_blog.py`: The Python engine.
- `markdown2`: To convert MD to HTML.
- `jinja2`: For templating.

## Logic
1. **Clear Public**: Delete all files in `/public`.
2. **Read Content**: Loop through `/content`, parse frontmatter and body.
3. **Generate Index JSON**: Create a list of all posts for the local search engine.
4. **Render Pages**: Inject content into templates and save to `/public`.
5. **Minify**: Ensure CSS/HTML are as small as possible.

## Edge Cases
- **Missing Frontmatter**: Log error and skip file.
- **Empty Description**: Use first 100 chars of body.
- **Broken Links**: Verify all internal links point to valid routes.
