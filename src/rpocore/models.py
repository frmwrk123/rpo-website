from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.pages.models import Page


class SupportGroup(models.Model):
    name = models.CharField(max_length=30, unique=True)
    total_amount = models.IntegerField(_('Total amount'))
    stretch_goals = models.CommaSeparatedIntegerField(_('Stretch goals'), max_length=255)

    def __str__(self):
        return self.name


class Supporter(models.Model):
    user = models.OneToOneField('auth.User')
    statement = models.TextField(
        _('Support statement'),
        null=True,
        help_text=_('This statement will appear on the list of supporters together with your name.')
    )
    support_group = models.ForeignKey(SupportGroup, on_delete=models.PROTECT, null=True)
    support_anonymous = models.BooleanField(
        _('Support anonymously'),
        help_text=_('If checked your name will not appear on the list of supporters.'),
        default=False
    )
    additional_information = models.CharField(
        _('Additional information'),
        max_length=50,
        blank=True,
        help_text=_('Here you can specify additional information about your activities, organizations, etc. It appears'
                    ' next to your name in the list of supporters.')
    )
    UNIVERSITIES = (
        ('UHH', 'Universität Hamburg'),
        ('TUHH', 'Technische Universität Hamburg'),
        ('HAW', 'Hochschule für Angewandte Wissenschaften Hamburg'),
        ('Other', 'Andere Universität oder Hochschule')
    )
    university = models.CharField(_('University'), choices=UNIVERSITIES, max_length=30, null=True)


class NotableSupporter(models.Model):
    name = models.CharField(max_length=30)
    position = models.CharField(_('Position'), max_length=50)
    FACULTIES = (
        ('MIN', 'MIN'),
        ('WiSo', 'WiSo'),
        ('BWL', 'BWL'),
        ('Recht', 'Recht'),
        ('Medizin', 'Medizin'),
        ('Erzwiss', 'Erzwiss'),
        ('GeiWi', 'GeiWi'),
        ('PB', 'Psychologie und Bewegungswissenschaften')
    )
    faculty = models.CharField(_('Faculty'), choices=FACULTIES, max_length=30)
    image = models.ImageField(_('Image'), upload_to='supporters/', blank=True)

    def __str__(self):
        return self.name


class SupporterPage(Page):
    notable_supporters = models.ManyToManyField(NotableSupporter, blank=True)


class FormalStatement(models.Model):
    organization = models.CharField(_('Organization'), max_length=30)
    file = models.FileField(_('File'), help_text=_('Only PDF files allowed'), upload_to='statements', blank=True)


class InformalStatement(models.Model):
    organization = models.CharField(_('Organization'), max_length=30)
    file = models.FileField(_('File'), help_text=_('Only PDF files allowed'), upload_to='statements')


class StatementPage(Page):
    formal_statements = models.ManyToManyField(FormalStatement, blank=True)
    informal_statements = models.ManyToManyField(InformalStatement, blank=True)
