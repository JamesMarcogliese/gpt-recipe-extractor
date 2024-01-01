import requests
from requests.auth import HTTPBasicAuth
import os
import re
import boto3
import json
from urllib.parse import unquote_plus

# RECALL > zip -r confluence_lambda_package.zip .

# Initialize the AWS S3 client
s3_client = boto3.client('s3')

# Read configuration from environment variables
CONFLUENCE_API_URL = os.environ['CONFLUENCE_API_URL']
CONFLUENCE_USERNAME = os.environ['CONFLUENCE_USERNAME']
API_TOKEN = os.environ['API_TOKEN']
SPACE_ID = os.environ['SPACE_ID']
PARENT_PAGE_ID = os.environ['PARENT_PAGE_ID']

auth = HTTPBasicAuth(CONFLUENCE_USERNAME, API_TOKEN)


# Function to check if a Confluence page with a given title already exists
def page_exists(title):
    headers = {"Accept": "application/json"}
    params = {
        "spaceId": SPACE_ID,
        "title": title
    }
    response = requests.get(CONFLUENCE_API_URL, headers=headers, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        return len(data.get("results")) > 0

    return False


# Function to create a new Confluence page from a Markdown file within a parent page
def create_page_within_parent(title, content):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "type": "page",
        "title": title,
        "spaceId": SPACE_ID,
        "parentId": PARENT_PAGE_ID,
        "status": "current",
        "body": {
            "value": content,
            "representation": "wiki"
        },
    }

    response = requests.post(CONFLUENCE_API_URL, headers=headers, json=payload, auth=auth)

    if response.status_code == 200:
        print(f"Page '{title}' created successfully within parent page ID {PARENT_PAGE_ID}.")
    else:
        print(f"Failed to create page '{title}' with status code {response.status_code}: {response.text}")


# Function to convert Markdown text to Confluence Wiki Markup
def markdown_to_confluence(markdown_text):
    """
    Converts Markdown text to Confluence Wiki Markup.
    """

    # Convert headers
    # Confluence Wiki Markup uses "h1.", "h2.", etc. for headers.
    markdown_text = re.sub(r'^#{1} (.*)', r'h1. \1', markdown_text, flags=re.MULTILINE)  # h1
    markdown_text = re.sub(r'^#{2} (.*)', r'h2. \1', markdown_text, flags=re.MULTILINE)  # h2
    markdown_text = re.sub(r'^#{3} (.*)', r'h3. \1', markdown_text, flags=re.MULTILINE)  # h3
    # Add more patterns for h4, h5, etc., if needed

    # Convert bullet points
    # Confluence uses "*" for bullet lists.
    markdown_text = re.sub(r'^- (.*)', r'* \1', markdown_text, flags=re.MULTILINE)

    # Additional conversions can be added here (italic, bold, links, images, etc.)

    return markdown_text


# Lambda handler function
def lambda_handler(event, context):
    # Process S3 event
    message = event['Records'][0]['body'] 

    message_json = json.loads(message) # SNS message is a string, not JSON, so covert it.
    print(message_json)
    # Extract bucket name and file key from the SQS message
    bucket_name = message_json['Records'][0]['s3']['bucket']['name']
    object_key = message_json['Records'][0]['s3']['object']['key']
    
    decoded_object_key = unquote_plus(object_key)

    # Get the markdown file from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=decoded_object_key)
    content = response['Body'].read().decode('utf-8')

    # Use the filename (without extension) as the page title
    page_title = os.path.splitext(os.path.basename(decoded_object_key))[0]

    # Check if the page already exists, and create it within the parent page if not
    if not page_exists(page_title):
        create_page_within_parent(page_title, markdown_to_confluence(content))
    else:
        print(f"Page '{page_title}' already exists. Skipping.")
