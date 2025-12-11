from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, GroupManager
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class CommonInfo(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_time = models.DateTimeField(auto_now_add=False, auto_now=True)


class Role(Group):
    objects = GroupManager()
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

class Company(models.Model):

    code = models.CharField(max_length=255, unique=True, help_text=_("Company Code"))
    name  = models.CharField( max_length=100, help_text=_("Company name"))
    is_active = models.BooleanField(_('Active'), default=True, help_text=_("Company holati"))
    phone = models.CharField(_("Phone number"), max_length=100, help_text=_("Telefon raqami"))
    region = models.ForeignKey("directory.Region", related_name='company_region', on_delete=models.SET_NULL, null=True,
                               help_text=_("Viloyat"))
    district = models.ForeignKey("directory.District", related_name='company_district', on_delete=models.SET_NULL,
                                 null=True, help_text=_("Tuman"))
    address = models.TextField(_("Address"), null=True, help_text=_("Yashash manzili"))
    created_time = models.DateTimeField(auto_now_add=True, help_text=_("Yaratilgan vaqt"))
    updated_time = models.DateTimeField(auto_now=True, help_text=_("Yangilangan vaqt"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='companies_created', null=True,
                                   on_delete=models.SET_NULL, help_text=_("Yaratgan foydalanuvchi"))
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='companies_updated', null=True,
                                   on_delete=models.SET_NULL, help_text=_("Yangilagan foydalanuvchi"))


    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    """
    Burn Community foydalanuvchisi (Telegram user).
    - Telegram ID, username, FIO, avatar, telefon, email, region va kategoriya saqlanadi.
    - points_balance: yuqori o‘ngdagi “b 0” ikonkasidagi ball balansi.
    - referral_code / referred_by: “Пригласить друга” referal dasturi uchun.
    - is_*_completed flaglar: profilni to‘ldirishdan bonus berish uchun maydonlar to‘lganligini belgilash.
    """

    class GENDERS(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')

    telegram_id = models.BigIntegerField(_('Telegram ID'), null=True, blank=True, unique=True)
    username = models.CharField(max_length=255, unique=True, help_text=_("Foydalanuvchi nomi"))
    fullname = models.CharField( max_length=100, help_text=_("Foydalanuvchi FIO"))
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d', null=True, blank=True, help_text=_("Profil rasmi"))
    date_of_birthday = models.DateField(_('date of birthday'), null=True, blank=True, help_text=_("Tug‘ilgan sanasi"))
    gender = models.CharField(choices=GENDERS.choices, max_length=6, null=True, blank=True, help_text=_("Jinsi"))
    phone_number = models.CharField(_("Phone number"), max_length=100, help_text=_("Telefon raqami"))
    email = models.EmailField(_('email address'), blank=True, null=True, help_text=_("Email manzili"))

    points_balance = models.PositiveIntegerField(_('Баланс баллов'), default=0)
    # Profilni to‘ldirishdan bonus berish uchun flaglar
    is_full_name_completed = models.BooleanField(default=False)
    is_phone_completed = models.BooleanField(default=False)
    is_email_completed = models.BooleanField(default=False)
    is_region_completed = models.BooleanField(default=False)
    is_category_completed = models.BooleanField(default=False)
    # "Пригласить друга”) uchun kerak. Har bir foydalanuvchiga unikal kod beriladi Masalan: BURN-1493477280
    referral_code = models.CharField( _('Реферальный код'), max_length=64, unique=True, null=True, blank=True,)
    # kim taklif qilganini saqlash.  Yangi foydalanuvchi botga kelganda, start dan kelgan kodni topamiz va osha kod orqali kim taklif qilganini saqlab qoyamiz
    referred_by = models.ForeignKey('self',verbose_name=_('Кем приглашён'), related_name='referrals', on_delete=models.SET_NULL, null=True, blank=True, )

    is_active = models.BooleanField(_('Active'), default=True, help_text=_("Foydalanuvchi holati"))
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True, help_text=_("Ro‘yxatdan o‘tgan sana"))
    password = models.CharField(max_length=255, null=True, blank=True, help_text=_("Parol"))
    region = models.ForeignKey("directory.Region", related_name='user_region', on_delete=models.SET_NULL, null=True,
                               help_text=_("Viloyat"))
    district = models.ForeignKey("directory.District", related_name='user_district', on_delete=models.SET_NULL,
                                 null=True, help_text=_("Tuman"))
    role = models.ForeignKey(Role, related_name='role_user', null=True, on_delete=models.SET_NULL,
                             help_text=_("Foydalanuvchi roli"))
    address = models.TextField(_("Address"), null=True, help_text=_("Yashash manzili"))
    created_time = models.DateTimeField(auto_now_add=True, help_text=_("Yaratilgan vaqt"))
    updated_time = models.DateTimeField(auto_now=True, help_text=_("Yangilangan vaqt"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_by_user', null=True,
                                   on_delete=models.SET_NULL, help_text=_("Yaratgan foydalanuvchi"))
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_by_user', null=True,
                                   on_delete=models.SET_NULL, help_text=_("Yangilagan foydalanuvchi"))

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        if self.fullname:
            return self.fullname
        if self.username:
            return self.username
        return str(self.pk)

    def is_admin(self) -> bool:
        return self.role and self.role.name == 'Administrator'


class AppModule(models.Model):
    name = models.CharField(_('Module name'), max_length=125, blank=True)
    on_dashboard = models.BooleanField(default=False)
    content_types = models.ManyToManyField(ContentType)
    sorting = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _('module')
        verbose_name_plural = _('modules')
