# 代码生成时间: 2025-09-21 20:16:53
import falcon
from falcon import HTTP_200, HTTP_500
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO

# Define the route for our Falcon API
API_ROUTE = '/generate-excel'

# Define the Excel generator class that handles requests
class ExcelGenerator:
    def on_get(self, req, resp):
        """
        Handle GET requests to generate an Excel file.
        Responds with an Excel file in the HTTP response.
        """
        try:
            # Create a Pandas DataFrame
            df = pd.DataFrame({'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']})

            # Create a new Excel workbook and add a worksheet
            workbook = Workbook()
            worksheet = workbook.active

            # Convert the DataFrame to rows and add them to the worksheet
            for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
                worksheet.append(row)

            # Save the workbook to a byte stream
            output = BytesIO()
            workbook.save(output)
            output.seek(0)

            # Set the response body to the Excel file and set the content type
            resp.body = output.getvalue()
            resp.content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            resp.status = HTTP_200
        except Exception as e:
            # Handle any exceptions and return a 500 Internal Server Error
            resp.status = HTTP_500
            resp.body = str(e)

# Initialize the Falcon API app
app = falcon.App()

# Add the route to the app with the Excel generator class
app.add_route(API_ROUTE, ExcelGenerator())

# This is a simple main function to run the API
if __name__ == '__main__':
    # Run the Falcon API
    import socket
    import threading
    from wsgiref.simple_server import make_server
    
    # Set the host and port for the API
    host = '127.0.0.1'
    port = 8000
    
    # Create a server and serve_forever
    httpd = make_server(host, port, app)
    print(f'Serving on {host}:{port}')
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    httpd.serve_forever()