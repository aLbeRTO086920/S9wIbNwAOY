# 代码生成时间: 2025-09-30 17:43:01
# batch_image_resizer.py
# A Falcon-based web service to resize multiple images in a batch

import falcon
import os
from PIL import Image
from io import BytesIO

class ImageResizer:
    """
    A Falcon resource class to handle image resizing requests.
    """
    def on_get(self, req, resp):
        """
        Handles GET requests to resize images.
        """
        # Check if the required parameter is present
        if 'path' not in req.params or 'target_width' not in req.params or 'target_height' not in req.params:
            raise falcon.HTTPBadRequest("Missing required parameters")

        path = req.params['path']
        target_width = int(req.params['target_width'])
        target_height = int(req.params['target_height'])

        # Ensure the path exists and is a directory
        if not os.path.isdir(path):
            raise falcon.HTTPError(f"Directory does not exist: {path}")

        # Walk through the directory and resize images
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                    try:
                        image_path = os.path.join(root, file)
                        with Image.open(image_path) as img:
                            img = img.resize((target_width, target_height))
                            buffer = BytesIO()
                            img.save(buffer, format=img.format.lower())
                            buffer.seek(0)
                            image_data = buffer.getvalue()

                            # Send the resized image back in the response
                            resp.content_type = 'image/' + img.format.lower()
                            resp.body = image_data
                    except IOError:
                        raise falcon.HTTPInternalServerError("Error resizing image")
                    except Exception as e:
                        raise falcon.HTTPInternalServerError(f"An unexpected error occurred: {e}")

    # Add support for POST requests to upload images for resizing
    def on_post(self, req, resp):
        """
        Handles POST requests to receive image data and resize it.
        """
        # Parse the request body as JSON
        try:
            body = req.media
            target_width = int(body['target_width'])
            target_height = int(body['target_height'])
            image_data = body['image_data']
        except (KeyError, ValueError):
            raise falcon.HTTPBadRequest("Invalid request body")
        except Exception as e:
            raise falcon.HTTPInternalServerError(f"An unexpected error occurred: {e}")

        try:
            # Load the image from the provided data
            with Image.open(BytesIO(image_data)) as img:
                img = img.resize((target_width, target_height))
                buffer = BytesIO()
                img.save(buffer, format=img.format.lower())
                buffer.seek(0)
                resized_image_data = buffer.getvalue()

                # Send the resized image back in the response
                resp.content_type = 'image/' + img.format.lower()
                resp.body = resized_image_data
        except IOError:
            raise falcon.HTTPInternalServerError(