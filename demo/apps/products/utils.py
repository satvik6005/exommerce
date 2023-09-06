from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import loader
from django.conf import settings as django_settings
from .models import product_order



class UserEmailFactoryBase(object):
    subject_template_name = None
    plain_body_template_name = None
    html_body_template_name = None

    def __init__(self, from_email, user, protocol, domain, site_name, **context):
        self.from_email = from_email
        self.user = user
        self.domain = domain
        self.site_name = site_name
        self.protocol = protocol
        self.context_data = context

    @classmethod
    def from_request(cls, request, user=None, from_email=None, **context):
        site = get_current_site(request)
        from_email = from_email or getattr(django_settings, "DEFAULT_FROM_EMAIL", "")

        return cls(
            from_email=from_email,
            user=user or request.user,
            domain=django_settings.ACCOUNTS.get("DOMAIN") or site.domain,
            site_name=django_settings.ACCOUNTS.get("SITE_NAME") or site.name,
            protocol="https" if request.is_secure() else "http",
            **context,
        )

    def create(self):
        assert self.plain_body_template_name or self.html_body_template_name
        context = self.get_context()
        subject = loader.render_to_string(self.subject_template_name, context)
        subject = "".join(subject.splitlines())

        if self.plain_body_template_name:
            plain_body = loader.render_to_string(self.plain_body_template_name, context)
            email_message = EmailMultiAlternatives(
                subject, plain_body, self.from_email, [self.user.email]
            )
            if self.html_body_template_name:
                html_body = loader.render_to_string(
                    self.html_body_template_name, context
                )
                email_message.attach_alternative(html_body, "text/html")
        else:
            print(context)
            html_body = loader.render_to_string(self.html_body_template_name, context)
            email_message = EmailMessage(
                subject, html_body, self.from_email, [self.user.email]
            )
            email_message.content_subtype = "html"
        return email_message

    def get_context(self):
        context = {
            "user": self.user,
            "domain": self.domain,
            "site_name": self.site_name,
            # "uid": encode_uid(self.user.pk),
            # "token": self.token_generator.make_token(self.user),
            "protocol": self.protocol,
        }
        context.update(self.context_data)
        return context
    
class UserPasswordResetEmailFactory(UserEmailFactoryBase):
    subject_template_name = "password_reset_email_subject.txt"
    plain_body_template_name = "password_reset_email_body.txt"

    def get_context(self):
        context = super(UserPasswordResetEmailFactory, self).get_context()
        context["url"] = django_settings.ACCOUNTS.get(
            "PASSWORD_RESET_CONFIRM_URL"
        ).format(**context)
        return context


class UserConfirmationEmailFactory(UserEmailFactoryBase):
    subject_template_name = "confirmation_email_subject.txt"
    plain_body_template_name = "confirmation_email_body.txt"

class order_invoice_genration_mail(UserEmailFactoryBase):
    html_body_template_name='invoice.html'
    subject_template_name='invoice_subject.txt'

    def get_order(self,order):
        self.order=order

    def get_context(self):
        context = super(order_invoice_genration_mail, self).get_context()
        context['user']=str(self.order.user.first_name)
        context['adress']=str(self.order.del_adress)
        context['order_id']=str(self.order.order_id)
        context['order_date']=str(self.order.date)
        context['products']=list(product_order.objects.filter(order=self.order))
        context['price']=self.order.final_price
        return context

        

            


