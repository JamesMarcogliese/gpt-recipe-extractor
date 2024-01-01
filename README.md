# GPT-4 Recipe Extractor

This repository contains resources for the GPT-4 Recipe Extractor, a tool that utilizes the OpenAI GPT-4 Vision model to extract recipes from images. The repository is organized into two main folders:

## CloudFormation

The `CloudFormation` folder contains AWS CloudFormation scripts and Lambda code for setting up an automated event-driven AWS architecture to process recipe images and/or upload them to a Confluence space. Here's an overview of its contents:

- `cloudformation_template.yml`: CloudFormation script defining AWS resources for processing recipe images. It includes IAM roles, S3 buckets, SQS queues, Lambda functions, and event triggers. This script automates the processing of images and markdown generation.

To get started with the AWS architecture, follow the instructions provided in the `CloudFormation` subfolder.

## Notebook

The `Notebook` folder contains Jupyter notebooks for manually running the recipe extraction code locally using the OpenAI GPT-4 Vision model. Here's an overview of its contents:

- `gpt-recipe-extractor.ipynb`: Jupyter notebook that demonstrates how to use the OpenAI GPT-4 Vision model to extract recipes from images. It supports both single-page and multi-page recipes.
- `confluence-recipe-uploader.ipynb`: Jupyter notebook that demonstrates how to upload the recipe markdown files to a Confluence space.

### Requirements

- Python 3
- `requests` library
- `glob` library
- OpenAI API key

### Limitations

The notebook assumes that the GPT-4 Vision model can accurately extract recipes from images. The accuracy of the extraction may vary depending on the quality and complexity of the images.

Feel free to explore and use the resources provided in this repository for automating recipe extraction and experimenting with the GPT-4 Vision model.

If you have any questions or encounter issues, please refer to the individual README files within each folder or reach out to the repository owner for assistance.

![High-Level Arch Vis](/images/gpt-recipe-extractor.png)