import base64
import requests
import os
import json
import re
import boto3
import time

# RECALL > zip -r gpt_lambda_package.zip .

# Initialize AWS S3 client
s3_client = boto3.client('s3')

# Read API key from environment variable
api_key = os.environ['API_KEY']

# Destination S3 bucket from environment variable
destination_bucket = os.environ['DESTINATION_BUCKET']

MAX_TOKENS = 4096
max_retries = 5

extraction_prompt = """
Attached is a magazine page containing one or more recipes. Please extract the following for each recipe in markdown format:
-Recipe name (with Heading level 1)
-Preparation time (with Heading level 2)
-Servings (with Heading level 2)
-Ingredients (with Heading level 2)
-Instructions (with Heading level 2)
-Cuisine name inferred from recipe (with Heading level 2)
"""


# Function to encode the image
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')


# Function to save markdown to S3
def save_markdown_to_s3(markdown, destination_bucket):
    recipes = re.split(r'\n# ', markdown)
    for i, recipe in enumerate(recipes):
        if i > 0:
            recipe = '# ' + recipe
        heading = re.search(r'^# (.*)$', recipe, re.MULTILINE)
        filename = heading.group(1) + '.md' if heading else f'default{i}.md'
        s3_client.put_object(Body=recipe, Bucket=destination_bucket, Key=f'{filename}')


# Lambda handler function
def lambda_handler(event, context):

    # Process S3 event
    message = event['Records'][0]['body']

    message_json = json.loads(message) # SNS message is a string, not JSON, so covert it.
    print(message_json)
    # Extract bucket name and file key from the SQS message
    bucket_name = message_json['Records'][0]['s3']['bucket']['name']
    object_key = message_json['Records'][0]['s3']['object']['key']

    # Get the image file from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_bytes = response['Body'].read()
    base64_image = encode_image(image_bytes)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": extraction_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": MAX_TOKENS
    }

    for i in range(max_retries):
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            markdown = json.loads(response.text)['choices'][0]['message']['content']
            save_markdown_to_s3(markdown, destination_bucket)
            s3_client.delete_object(Bucket=bucket_name, Key=object_key)
            break
        except requests.exceptions.RequestException as e:
            wait_time = 2 ** i
            print(f"Request failed with error {e}. Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    else:
        print(f"Failed to process image {object_key} after {max_retries} retries.")
