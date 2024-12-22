
from django.contrib import admin
from django.http import HttpResponse
import openpyxl
from reportlab.pdfgen import canvas
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    actions = ['export_to_excel', 'export_to_pdf']

    # Export selected contacts to Excel
    def export_to_excel(self, request, queryset):
        # Create Excel workbook
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Contacts"

        # Add headers
        headers = ['Name', 'Email', 'Subject', 'Message', 'Created At']
        sheet.append(headers)

        # Add data rows
        for contact in queryset:
            sheet.append([
                contact.name,
                contact.email,
                contact.subject,
                contact.message,
                contact.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            ])

        # Create HTTP response
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename=contacts.xlsx'
        workbook.save(response)
        return response

    export_to_excel.short_description = "Export Selected to Excel"

    # Export selected contacts to PDF
    def export_to_pdf(self, request, queryset):
        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=contacts.pdf'

        # Create PDF canvas
        p = canvas.Canvas(response)
        p.setFont("Helvetica", 12)
        p.drawString(100, 800, "Contact Form Submissions")
        y = 750

        for contact in queryset:
            line = f"Name: {contact.name}, Email: {contact.email}, Subject: {contact.subject}, Message: {contact.message}, Date: {contact.created_at.strftime('%Y-%m-%d')}"
            p.drawString(50, y, line)
            y -= 20

        p.save()
        return response

    export_to_pdf.short_description = "Export Selected to PDF"

    # Add custom context for changelist view (e.g., for download links)
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['download_excel_url'] = '/admin/contacts/export/excel/'
        extra_context['download_pdf_url'] = '/admin/contacts/export/pdf/'
        return super().changelist_view(request, extra_context=extra_context)
