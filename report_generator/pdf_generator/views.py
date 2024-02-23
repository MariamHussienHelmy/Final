
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fpdf import FPDF
import requests
import webcolors
import json
def get_color_from_name(color_name):
    try:
        color = webcolors.name_to_rgb(color_name)
        return color
    except ValueError:
        return None

@csrf_exempt
def generate_pdf(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            kit_code = data.get('Kit_code')
            if kit_code:
                headers = {'Authorization': 'Token dda14349bf903bb808411eb7874d34902b3c23ff'}
                git_response = requests.get(f'https://magisnatomicsapp.org/api/final_report/{kit_code}/', headers=headers)
                if git_response.status_code == 200:
                    report_data = git_response.json()
                    snps_info = report_data.get('SNPs_info', [])
                    generate_colored_pdf(snps_info, report_data)
                    return JsonResponse({'message': 'PDF generated successfully.'}, status=200)
                else:
                    return JsonResponse({'error': 'Failed to fetch data from Git API.'}, status=500)
            else:
                return JsonResponse({'error': 'Invalid request. "Kit_code" parameter missing.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

def generate_colored_pdf(color_data, report_data):
    pdf = FPDF()
    pdf.add_page()
    
    # Set font styles
    title_font = ('Arial', 'B', 16)
    header_font = ('Arial', 'B', 12)
    body_font = ('Arial', '', 12)
    
    # Add report title
    pdf.set_font(*title_font)
    pdf.cell(200, 10, "Genetic Analysis Report", ln=True, align='C')
    pdf.ln(10)  # Add some space after the title
    
    # Add customer information
    pdf.set_font(*header_font)
    customer_info = report_data.get('Customer_info', {})
    pdf.cell(0, 10, f"Customer Name: {customer_info.get('First_name')} {customer_info.get('Last_name')}", ln=True)
    pdf.cell(0, 10, f"Date of Birth: {customer_info.get('Date_of_birth')}", ln=True)
    pdf.cell(0, 10, f"Address: {customer_info.get('Address')}, {customer_info.get('City')}, {customer_info.get('State')} {customer_info.get('ZIP_code')}", ln=True)
    pdf.cell(0, 10, f"Email: {customer_info.get('Email')}", ln=True)
    pdf.ln(10)  # Add some space after the customer information
    
    # Calculate column widths dynamically based on text length
    column_widths = [40, 80]
    for item in color_data:
        gene_width = pdf.get_string_width(item.get('Gene')) + 6  # Add padding
        outcome_width = pdf.get_string_width(item.get('Outcome')) + 6  # Add padding
        column_widths[0] = max(column_widths[0], gene_width)
        column_widths[1] = max(column_widths[1], outcome_width)
    
    # Add table headers
    pdf.set_font(*header_font)
    pdf.set_fill_color(200, 200, 200)  # Gray background for headers
    pdf.cell(column_widths[0], 10, "Gene", border=1, fill=True)
    pdf.cell(column_widths[1], 10, "Outcome", border=1, fill=True)
    pdf.ln()  # Move to the next line
    
    # Add SNP information
    pdf.set_font(*body_font)
    for item in color_data:
        gene = item.get('Gene')
        outcome = item.get('Outcome')
        color_name = item.get('Color')
        
        # Convert color name to RGB values
        if color_name.startswith('#'):
            color_rgb = webcolors.hex_to_rgb(color_name)
        else:
            color_rgb = webcolors.name_to_rgb(color_name)
        
        pdf.set_text_color(*color_rgb)
        
        pdf.cell(column_widths[0], 10, gene, border=1)
        pdf.cell(column_widths[1], 10, outcome, border=1)
        pdf.ln()  # Move to the next line
        
        # Check if adding a new page is required
        if pdf.get_y() > 250:  # Example height limit for adding page numbers
            pdf.add_page()
            if pdf.page_no() != 1:  # Exclude main page
                pdf.set_font('Arial', 'I', 10)
                pdf.cell(0, 10, f'Page {pdf.page_no()}', 0, 0, 'R')  # Add page number at the bottom right corner
            pdf.ln()

    # Add page number at the bottom of the last page
    if pdf.page_no() != 1:  # Exclude main page
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 10, f'Page {pdf.page_no()}', 0, 0, 'R')  # Add page number at the bottom right corner

    pdf.output("colored_items.pdf")
    pdf = FPDF()
    pdf.add_page()
    
    # Set font styles
    title_font = ('Arial', 'B', 16)
    header_font = ('Arial', 'B', 12)
    body_font = ('Arial', '', 12)
    
    # Add report title
    pdf.set_font(*title_font)
    pdf.cell(200, 10, "Genetic Analysis Report", ln=True, align='C')
    pdf.ln(10)  # Add some space after the title
    
    # Add customer information
    pdf.set_font(*header_font)
    customer_info = report_data.get('Customer_info', {})
    pdf.cell(0, 10, f"Customer Name: {customer_info.get('First_name')} {customer_info.get('Last_name')}", ln=True)
    pdf.cell(0, 10, f"Date of Birth: {customer_info.get('Date_of_birth')}", ln=True)
    pdf.cell(0, 10, f"Address: {customer_info.get('Address')}, {customer_info.get('City')}, {customer_info.get('State')} {customer_info.get('ZIP_code')}", ln=True)
    pdf.cell(0, 10, f"Email: {customer_info.get('Email')}", ln=True)
    pdf.ln(10)  # Add some space after the customer information
    
    # Calculate column widths dynamically based on text length
    column_widths = [40, 80]
    for item in color_data:
        gene_width = pdf.get_string_width(item.get('Gene')) + 6  # Add padding
        outcome_width = pdf.get_string_width(item.get('Outcome')) + 6  # Add padding
        column_widths[0] = max(column_widths[0], gene_width)
        column_widths[1] = max(column_widths[1], outcome_width)
    
    # Add table headers
    pdf.set_font(*header_font)
    pdf.set_fill_color(200, 200, 200)  # Gray background for headers
    pdf.cell(column_widths[0], 10, "Gene", border=1, fill=True)
    pdf.cell(column_widths[1], 10, "Outcome", border=1, fill=True)
    pdf.ln()  # Move to the next line
    
    # Add SNP information
    pdf.set_font(*body_font)
    for item in color_data:
        gene = item.get('Gene')
        outcome = item.get('Outcome')
        color_name = item.get('Color')
        
        # Convert color name to RGB values
        if color_name.startswith('#'):
            color_rgb = webcolors.hex_to_rgb(color_name)
        else:
            color_rgb = webcolors.name_to_rgb(color_name)
        
        pdf.set_text_color(*color_rgb)
        
        pdf.cell(column_widths[0], 10, gene, border=1)
        pdf.cell(column_widths[1], 10, outcome, border=1)
        pdf.ln()  # Move to the next line
        
        # Check if adding a new page is required
        if pdf.get_y() > 250:  # Example height limit for adding page numbers
            pdf.add_page()
            # Add page number at the bottom
            pdf.set_font('Arial', 'I', 10)
            pdf.cell(0, 10, f'Page {pdf.page_no()}', 0, 0, 'C')
            pdf.ln()

    # Add page number at the bottom of the last page
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f'Page {pdf.page_no()}', 0, 0, 'C')

    pdf.output("colored_items.pdf")