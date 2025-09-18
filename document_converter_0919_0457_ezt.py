# 代码生成时间: 2025-09-19 04:57:23
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Document Converter using Falcon Framework
A simple API service that converts documents from one format to another.
"""

import falcon
import json
from docx import Document
from falcon import HTTP_200, HTTP_400, HTTP_500

# Define the supported document formats
SUPPORTED_FORMATS = {'docx', 'txt'}

class DocumentConverter:
    """
    A simple class that handles document conversion.
    """"
    def on_get(self, req, resp):
        """
        Handles GET requests by returning a list of supported formats.
        """"
        resp.media = {'formats': list(SUPPORTED_FORMATS)}
        resp.status = HTTP_200

    def on_post(self, req, resp):
        """
        Handles POST requests by attempting to convert a document.
        """"
        try:
            # Parse the JSON request body
            doc_data = req.media.get('document')
            target_format = req.media.get('target_format')

            # Check if the target format is supported
            if target_format not in SUPPORTED_FORMATS:
                raise falcon.HTTPError(falcon.HTTP_400, 'Invalid target format.', 'Unsupported format.')

            # Convert the document (simplified for demonstration)
            if target_format == 'txt':
                # Simulate conversion by just returning the content as text
                resp.media = {'content': str(doc_data)}
            else:
                # Default to returning the document as is (e.g., no conversion needed)
                resp.media = {'content': doc_data}

            resp.status = HTTP_200
        except (KeyError, ValueError, TypeError) as e:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid request.', str(e))
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_500, 'Internal Server Error.', str(e))

def create_app():
    """
    Creates and returns the Falcon app.
    """
    app = falcon.App()
    # Register the 'DocumentConverter' resource for handling requests
    app.add_route('/documents', DocumentConverter())
    return app

# The main function that starts the Falcon API service
if __name__ == '__main__':
    app = create_app()
    # Run the app on localhost with port 8000 by default
    app.run(host='localhost', port=8000)