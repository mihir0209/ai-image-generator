import boto3
import os
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Triggered when image is uploaded to S3
    Creates a 200x200 thumbnail and saves to thumbnails/ folder
    """
    try:
        # Get bucket and key from event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # Skip if already a thumbnail
        if key.startswith('thumbnails/'):
            return {'statusCode': 200, 'body': 'Already a thumbnail'}
        
        # Download original image
        response = s3.get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()
        
        # Open image with Pillow
        img = Image.open(io.BytesIO(image_data))
        
        # Create thumbnail (200x200)
        img.thumbnail((200, 200), Image.Resampling.LANCZOS)
        
        # Save to bytes
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Generate thumbnail key
        filename = key.split('/')[-1]
        thumbnail_key = f'thumbnails/{filename}'
        
        # Upload thumbnail to S3
        s3.put_object(
            Bucket=bucket,
            Key=thumbnail_key,
            Body=buffer,
            ContentType='image/png'
        )
        
        print(f'Thumbnail created: {thumbnail_key}')
        
        return {
            'statusCode': 200,
            'body': f'Thumbnail created: {thumbnail_key}'
        }
        
    except Exception as e:
        print(f'Error creating thumbnail: {str(e)}')
        return {
            'statusCode': 500,
            'body': str(e)
        }
