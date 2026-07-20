# Akkireddy Challa Portfolio

This repository powers [akkireddy-challa.github.io](https://akkireddy-challa.github.io/), the public portfolio and writing hub for Akkireddy Challa.

## Focus

- Multi-cloud platform engineering across GCP, AWS, and Azure
- DevOps, SRE, CI/CD, infrastructure as code, and automation
- Observability, FinOps, IAM, and reliable production foundations
- Data and AI platform infrastructure, including GKE, Vertex AI, BigQuery, EKS, MSK, and Redshift Serverless
- Open-source learning history and practical engineering writing

## Structure

- `index.html` - portfolio content and metadata
- `blog.html` - writing index
- `writing/` - long-form engineering articles
- `writing/_post-template.html` - copyable starting point for a new article
- `css/styles.css` - responsive visual design
- `images/` - resume and visual assets
- `libs/font-awesome/` - icon font used by footer links
- `robots.txt` and `sitemap.xml` - basic search indexing support

The site is static and can be opened directly in a browser or served by GitHub Pages.

## Writing Topics

- Cloud platform operating models
- Terraform best practices
- Observability foundations
- AI infrastructure foundations

## Maintenance

Keep the site lightweight: static HTML, one CSS file, local assets, and no unnecessary build dependencies. To publish a post, copy `writing/_post-template.html`, replace its placeholders, link it from `blog.html`, add it to `feed.xml` and `sitemap.xml`, and update its neighbouring article links.
