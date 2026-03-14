# Work Item: Add markdown parser

**ID**: add-markdown-parser  
**Intent**: create-markdown-storage  
**Status**: pending  
**Complexity**: medium  
**Mode**: confirm

## Description

Add markdown and frontmatter parsing utilities.

## Files to Create

- `src/storage/parser.py` - Markdown/frontmatter parser

## Requirements

- Parse YAML frontmatter
- Extract metadata from frontmatter
- Parse markdown body content
- Handle edge cases (no frontmatter, malformed YAML)

## Dependencies

- pyyaml

## Acceptance Criteria

- Can parse markdown with frontmatter
- Can generate markdown from dict + content
- Round-trip parsing works
