"""
Renderers are used to serialize a response into specific media types.

They give us a generic way of being able to handle various media types
on the response, such as JSON encoded data or HTML output.
"""
import io
import os
import ssl

import pandas as pd
from rest_framework import status
from rest_framework.renderers import BaseRenderer, TemplateHTMLRenderer


class ExcelRenderer(BaseRenderer):
    """
    Renderer which serializes to Excel.
    """
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    format = 'xlsx'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into Excel.
        """
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        df = pd.DataFrame(data)
        sheet_name = data.serializer.sheet_name if hasattr(data.serializer, 'sheet_name') else 'Sheet1'
        startrow = data.serializer.startrow if hasattr(data.serializer, 'startrow') else 0
        df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=startrow)
        if hasattr(data.serializer, 'format_excel_output'):
            data.serializer.format_excel_output(writer)

        writer.save()
        return output.getvalue()


class PDFRenderer(TemplateHTMLRenderer):
    """
    A PDF renderer for use with templates.

    The data supplied to the Response object should be a dictionary that will
    be used as context for the template.

    The template name is determined by (in order of preference):

    1. An explicit `.template_name` attribute set on the response.
    2. An explicit `.template_name` attribute set on this class.
    3. The return result of calling `view.get_template_names()`.

    For example:
        data = {'users': User.objects.all()}
        return Response(data, template_name='users.html')
    """
    media_type = 'application/pdf'
    format = 'pdf'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders data to PDF, using Django's standard template rendering.

        The template name is determined by (in order of preference):

        1. An explicit .template_name set on the response.
        2. An explicit .template_name set on this class.
        3. The return result of calling view.get_template_names().
        """
        request, response = renderer_context['request'], renderer_context['response']
        if response.status_code == status.HTTP_200_OK:
            content = super().render(data, accepted_media_type, renderer_context)
            from weasyprint import HTML
            if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
                ssl._create_default_https_context = ssl._create_unverified_context
            return HTML(string=content, base_url=request.build_absolute_uri('/')).write_pdf()
        else:
            response['Content-Type'] = "{0}; charset={1}".format(super().media_type, super().charset)
            return super().render(data, accepted_media_type, renderer_context)
