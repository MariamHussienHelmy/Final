import json
import requests
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


@csrf_exempt
def generate_report(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST requests are allowed.")

    try:
        data = json.loads(request.body)
        kit_code = data.get('kit_code')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON data.")

    if not kit_code:
        return HttpResponseBadRequest("Kit code is missing in the request.")

    url = f"https://magisnatomicsapp.org/api/final_report/{kit_code}/"
    headers = {'Authorization': 'Token dda14349bf903bb808411eb7874d34902b3c23ff'}  # Add the Authorization header
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return HttpResponseBadRequest("Failed to fetch data from the API.")

    try:
        api_data = response.json()
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Failed to parse JSON data from the API.")

    # Create a new PDF
    pdf_filename = f"report_{kit_code}.pdf"
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)

    # Initialize starting position for text drawing
    x_position = 100
    y_position = 700

    if isinstance(api_data, dict):
        for key, value in api_data.items():
            if key == "Color":
                # Set the fill color for subsequent text drawing
                pdf.setFillColor(colors.HexColor(value))
            else:
                # For other keys, draw the text with the specified color and update position
                pdf.drawString(x_position, y_position, f"{key}: {value}")
                y_position -= 20  # Move to the next line

    # Save the PDF
    pdf.save()

    return JsonResponse({'message': 'PDF generated successfully', 'pdf_filename': pdf_filename})