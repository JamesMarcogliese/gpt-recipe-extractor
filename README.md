# GPT-4 Recipe Extractor

This Jupyter notebook uses the OpenAI GPT-4 Vision model to extract recipes from images. It supports both single-page, multi-page, and multi-recipe-on-single-page images.

## How it works

The notebook scans a source directory for images of recipes. For multi-page recipes, each recipe should be in its own subfolder within the source directory. The images are then sent to the GPT-4 Vision model, which returns the extracted recipe in markdown format. The markdown is saved to a destination directory.

The notebook also includes error handling with exponential backoff. If a request to the GPT-4 Vision model fails, the notebook will retry the request with an increasing wait time between each attempt.

## Usage

1. Set your OpenAI API key in a `key.txt` file in the root folder.
2. Place single-page recipe JPG images in a `source_folder_single_page` folder.
3. Place multiple-page recipe JPG images within subfolders (folder names are unimportant) in a `source_folder_multi_page` folder.
4. Run the notebook.

## Requirements

- Python 3
- `requests` library
- `glob` library
- OpenAI API key

## Limitations

The notebook assumes that the GPT-4 Vision model can accurately extract recipes from images. The accuracy of the extraction may vary depending on the quality and complexity of the images.