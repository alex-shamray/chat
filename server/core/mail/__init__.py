from email.mime.image import MIMEImage

from django.template import loader

from .message import EmailMultiRelated


def send_mail(subject_template_name, email_template_name,
              context, from_email, to_email, html_email_template_name=None, images={}):
    """
    Sends a core.mail.EmailMultiRelated to `to_email`.
    """
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiRelated(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')
    for name, fp in images.items():
        fp.seek(0)
        image = MIMEImage(fp.read(), 'related')
        # https://djangosnippets.org/snippets/2215/
        image.add_header('Content-Disposition', 'inline', filename=name)
        image.add_header('Content-ID', '<{}>'.format(name))
        email_message.attach(image)

    email_message.send()
