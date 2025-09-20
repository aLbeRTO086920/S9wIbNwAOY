# 代码生成时间: 2025-09-20 14:22:26
#!/usr/bin/env python

"""
A simple Falcon app demonstrating XSS protection.
"""
import falcon
from html import escape


# Function to sanitize input to prevent XSS attacks
def sanitize_input(input_str):
    """
    Sanitizes the input to prevent XSS attacks by escaping HTML special characters.
# 增强安全性

    Args:
    input_str (str): The input string to be sanitized.

    Returns:
    str: The sanitized string.
# TODO: 优化性能
    """
    return escape(input_str)

# Falcon route handler
# NOTE: 重要实现细节
class XssProtectedResource:
    """
    Resource that handles GET requests, demonstrating XSS protection.
    """
    def on_get(self, req, resp):
# TODO: 优化性能
        """
        Handle GET requests.
        """
        # Retrieve user input from query parameters
        user_input = req.get_param('input', default='')

        # Sanitize user input to prevent XSS attacks
        sanitized_input = sanitize_input(user_input)
# NOTE: 重要实现细节

        # Respond with sanitized input
        resp.media = {'sanitized_input': sanitized_input}

# Create the Falcon API app
app = falcon.App()

# Add a route with the XssProtectedResource handler
app.add_route('/xss-protect', XssProtectedResource())

# Error handler
# 扩展功能模块
@app.error_handler(falcon.HTTPBadRequest)
def handle_400(req, resp, ex):
    """
    Handles 400 Bad Request errors.
    """
    resp.media = {'status': 'error', 'message': 'Bad request'}
    resp.status = falcon.HTTP_400
# 扩展功能模块

# Ensure the app runs in a WSGI server
if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('localhost', 8000, app)
    print('Serving on localhost port 8000...')
    httpd.serve_forever()