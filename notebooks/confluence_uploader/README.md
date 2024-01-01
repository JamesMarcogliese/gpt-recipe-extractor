# confluence-recipe-uploader

This Jupyter notebook uploads markdown recipes to an Atlassian Confluence space. It converts input standard Markdown format into Atlassian 'Wiki' style Markdown accepted by Confluence.

## How it works

The notebook scans a source directory for markdown files of recipes, then checks to see if a page already exists under the parent/space you specify. If it does not exist, it is created.

## Usage

1. Fill in the configurations in the notebook under 'Configurations'.
2. Place Markdown recipe files in `input_markdown` folder.
3. Run the notebook.

## Requirements

- Python 3
- `requests` library
