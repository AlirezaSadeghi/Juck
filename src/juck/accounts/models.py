# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from django.db import models
from django.utils import timezone
from juck.image.models import JuckImage


class State(models.Model):
    class Meta:
        verbose_name = u"استان"
        verbose_name_plural = u"استان‌ها"

    name = models.CharField(max_length=100, blank=False, null=True, verbose_name=u'نام استان')

    def pair_renderer(self):
        cities = self.cities.select_related().all()

        return_value = []
        for city in cities:
            return_value.append((city.pk, city.name))

        return return_value

    def __unicode__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name = u'شهر'
        verbose_name_plural = u'شهرها'

    state = models.ForeignKey(State, related_name='cities', verbose_name=u'نام استان')

    name = models.CharField(max_length=100, verbose_name=u'نام شهر')


    def __unicode__(self):
        return self.name


class JobSeekerProfile(models.Model):
    class Meta:
        verbose_name = u'پروفایل کارجو'
        verbose_name_plural = u'پروفایل کارجویان'

    city = models.ForeignKey(City, verbose_name=u'شهر', related_name='jobseekerprofiles')
    state = models.ForeignKey(State, verbose_name=u'استان', related_name='jobseekerprofiles')
    national_id = models.CharField(max_length=20, verbose_name=u'کد ملی')
    date_of_birth = models.DateField(verbose_name=u'تاریخ تولد', blank=True, null=True)
    sex = models.PositiveSmallIntegerField(verbose_name=u'جنسیت', choices=((1, u'مرد'), (2, u'زن'), (3, u'دیگر'), ))
    married = models.BooleanField(verbose_name=u'وضعیت تاهل ', choices=((False, u'مجرد'), (True, u'متاهل'), ))
    image = models.ForeignKey(JuckImage, verbose_name=u'عکس پروفایل', null=True, blank=True)
    phone_number = models.CharField(verbose_name=u'شماره تلفن', max_length=20, null=True, blank=True)
    mobile_number = models.CharField(verbose_name=u'شماره همراه', max_length=25)
    military_service_status = models.CharField(verbose_name=u'وضعیت نظام وظیفه', max_length=100)
    exemption_type = models.CharField(verbose_name=u'نوع معافیت', max_length=100)

    approved = models.BooleanField(verbose_name=u'وضعیت تایید', default=False)


class EmployerProfile(models.Model):
    class Meta:
        verbose_name = u'پروفایل کارفرما'
        verbose_name_plural = u'پروفایل کارفرمایان'

    city = models.ForeignKey(City, verbose_name=u'شهر', related_name='employerprofiles')
    state = models.ForeignKey(State, verbose_name=u'استان', related_name='employerprofiles')

    company_name = models.CharField(max_length=200, verbose_name=u'نام سازمان')
    company_type = models.CharField(max_length=150, verbose_name=u'نوع سازمان')
    foundation_year = models.IntegerField(verbose_name=u'سال تاسیس')
    reg_num = models.CharField(max_length=100, verbose_name=u'شماره ثبت')
    manager = models.CharField(max_length=250, verbose_name=u'مشخصات مدیر عامل', null=True, blank=True)
    user_rank = models.CharField(max_length=150, verbose_name=u'سمت شخص رابط', null=True, blank=True)
    field = models.CharField(max_length=200, verbose_name=u'زمینه فعالیت')
    address = models.TextField(u'آدرس')
    postal_code = models.CharField(max_length=50, verbose_name=u'کد پستی', null=True, blank=True)
    phone_number = models.CharField(verbose_name=u'شماره تلفن', max_length=20)
    mobile_number = models.CharField(verbose_name=u'شماره همراه', max_length=25, null=True, blank=True)
    website = models.CharField(verbose_name=u'تارنما', max_length=200, blank=True, null=True)

    approved = models.BooleanField(verbose_name=u'وضعیت تایید', default=False)


class JuckUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(u'رایانامه باید تعیین شود')

        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_active=True, is_admin=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_active = True
        u.is_admin = True
        u.save(using=self._db)
        return u



class JuckUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = u'کاربر'
        verbose_name_plural = u'کاربران'

    email = models.EmailField(
        verbose_name='پست الکترونیک',
        max_length=255,
        unique=True,
        db_index=True,
    )

    first_name = models.CharField(verbose_name=u'نام', max_length=100, blank=True)
    last_name = models.CharField(verbose_name=u'نام خانوادگی', max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(u'date joined', default=timezone.now)

    objects = JuckUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return u' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.last_name

    def __unicode__(self):
        return self.email

    # TODO : Na'h, think about sth to make it right
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Manager(JuckUser):
    class Meta:
        verbose_name = u'مدیر'
        verbose_name_plural = u'مدیران'
        permissions = (
            ('superuser', u'مشاهده موارد مدیریتی'),
        )


class Employer(JuckUser):
    class Meta:
        verbose_name = u'کارفرما'
        verbose_name_plural = u'کارفرمایان'


    def __unicode__(self):
        return self.name

    profile = models.OneToOneField(EmployerProfile, verbose_name=u'پروفایل کارفرما', related_name='employer')


class JobSeeker(JuckUser):
    class Meta:
        verbose_name = u'کارجو'
        verbose_name_plural = u'کارجویان'

    def __unicode__(self):
        return self.name

    profile = models.OneToOneField(JobSeekerProfile, verbose_name=u'پروفایل کارجو', related_name='jobseeker')


class TemporaryLink(models.Model):
    class Meta:
        verbose_name = u'لینک موقت'
        verbose_name_plural = u'لینک های موقت'


    url_hash = models.CharField(u'لینک', max_length=120, unique=True)
    expire_date = models.DateTimeField(u'زمان ابطال')
    email = models.EmailField(u'پست الکترونیکی')

    def __unicode__(self):
        return self.email + str(self.expire_date.date())