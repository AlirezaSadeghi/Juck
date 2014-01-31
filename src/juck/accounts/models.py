# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from django.db import models
from django.utils import timezone
from juck.image.models import JuckImage
from django.conf import settings


class State(models.Model):
    class Meta:
        verbose_name = u"استان"
        verbose_name_plural = u"استان‌ها"

    name = models.CharField(max_length=100, blank=False, null=True, verbose_name=u'نام استان', unique=True)

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

    name = models.CharField(max_length=100, verbose_name=u'نام شهر', unique=True)


    def __unicode__(self):
        return self.name


class JobSeekerProfile(models.Model):
    class Meta:
        verbose_name = u'پروفایل کارجو'
        verbose_name_plural = u'پروفایل کارجویان'

    city = models.ForeignKey(City, verbose_name=u'شهر', related_name='jobseekerprofiles')
    state = models.ForeignKey(State, verbose_name=u'استان', related_name='jobseekerprofiles')
    national_id = models.CharField(max_length=20, verbose_name=u'کد ملی', unique=True)
    date_of_birth = models.DateField(verbose_name=u'تاریخ تولد', blank=True, null=True)
    sex = models.PositiveSmallIntegerField(verbose_name=u'جنسیت', blank=True, null=True)
    married = models.BooleanField(verbose_name=u'وضعیت تاهل', blank=True, default=False)
    image = models.ForeignKey(JuckImage, verbose_name=u'عکس پروفایل', null=True, blank=True)
    phone_number = models.CharField(verbose_name=u'شماره تلفن', max_length=20)
    mobile_number = models.CharField(verbose_name=u'شماره همراه', max_length=25, null=True, blank=True)
    military_service_status = models.CharField(verbose_name=u'وضعیت نظام وظیفه', max_length=100, null=True, blank=True)
    exemption_type = models.CharField(verbose_name=u'نوع معافیت', max_length=100, null=True, blank=True)

    approved = models.BooleanField(verbose_name=u'وضعیت تایید', default=False)

    # def __unicode__(self):
    #     return self.jobseeker.email


class EmployerProfile(models.Model):
    class Meta:
        verbose_name = u'پروفایل کارفرما'
        verbose_name_plural = u'پروفایل کارفرمایان'

    city = models.ForeignKey(City, verbose_name=u'شهر', related_name='employerprofiles')
    state = models.ForeignKey(State, verbose_name=u'استان', related_name='employerprofiles')

    company_name = models.CharField(max_length=200, verbose_name=u'نام سازمان')
    company_type = models.CharField(max_length=150, verbose_name=u'نوع سازمان')
    foundation_year = models.IntegerField(verbose_name=u'سال تاسیس')
    image = models.ForeignKey(JuckImage, verbose_name=u'لوگو سازمان', null=True, blank=True)
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

    # def __unicode__(self):
    #     return self.employer


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
        u.role = 4
        u.save(using=self._db)
        return u


class JuckUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = u'کاربر'
        verbose_name_plural = u'کاربران'

    email = models.EmailField(
        verbose_name=u'نام کاربری',
        max_length=255,
        unique=True,
        db_index=True,
    )

    JOB_SEEKER = 3
    MANAGER = 1
    EMPLOYER = 2

    USER_CHOICES = (
        (1, u'مدیر'),
        (2, u'کارفرما'),
        (3, u'کارجو'),
    )

    first_name = models.CharField(verbose_name=u'نام', max_length=100, blank=True)
    last_name = models.CharField(verbose_name=u'نام خانوادگی', max_length=150, blank=True)

    role = models.IntegerField(default=1, verbose_name=u'نوع کاربری', choices=USER_CHOICES)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(u'زمان عضویت', default=timezone.now)

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
        # return self.profile.company_name
        return self.email

    profile = models.OneToOneField(EmployerProfile, verbose_name=u'پروفایل کارفرما', related_name='employer')

    activation_key = models.CharField(verbose_name=u'کد فعال‌سازی', max_length=200, blank=True, null=True)

    def get_rate(self):
        ratings = self.ratings.all()

        rate = 0.0
        for item in ratings:
            rate += item.rate

        return round(rate / len(ratings))


class JobSeeker(JuckUser):
    class Meta:
        verbose_name = u'کارجو'
        verbose_name_plural = u'کارجویان'


    def __unicode__(self):
        return self.email

    profile = models.OneToOneField(JobSeekerProfile, verbose_name=u'پروفایل کارجو', related_name='jobseeker')
    resume = models.OneToOneField('Resume', verbose_name=u'رزومه', null=True, blank=True, related_name='jobseeker')

    activation_key = models.CharField(verbose_name=u'کد فعال‌سازی', max_length=200, blank=True, null=True)


    def get_rate(self):
        ratings = self.ratings.all()

        rate = 0.0
        for item in ratings:
            rate += item.rate

        return round(rate / len(ratings))


class Education(models.Model):
    class Meta:
        verbose_name_plural = u'اطلاعات تحصیلات'
        verbose_name = u'اطلاعات تحصیلی'

    certificate = models.CharField(verbose_name=u'مدرک تحصیلی', max_length=100,
                                   choices=(
                                       ('under_grad', u'کارشناسی'),
                                       ('grad', u'کارشناسی ارشد'),
                                       ('phd', u'دکتری'),
                                       ('post_doc', u'پست دکتری'),
                                   ))
    status = models.CharField(verbose_name=u'وضعیت تحصیلی', max_length=100)
    major = models.CharField(verbose_name=u'رشته تحصیلی', max_length=200)
    orientation = models.CharField(verbose_name=u'گرایش تحصیلی', max_length=150)
    university_name = models.CharField(max_length=150, verbose_name=u'نام دانشگاه')
    university_type = models.CharField(verbose_name=u'نوع دانشگاه', max_length=100)

    def __unicode__(self):
        return " ".join([self.status, self.certificate, self.orientation, self.major, self.university_name])


class Experience(models.Model):
    class Meta:
        verbose_name = u'سابقه'
        verbose_name_plural = u'سوابق'

    #resume = models.ForeignKey('Resume', verbose_name=u'رزومه', related_name='experiences')
    title = models.CharField(max_length=200, verbose_name=u'عنوان سابقه')
    place = models.CharField(max_length=200, verbose_name=u'سازمان یا دانشگاه مربوطه')
    from_date = models.DateField(verbose_name=u'از تاریخ')
    to_date = models.DateField(verbose_name=u'تا تاریخ')
    description = models.TextField(verbose_name=u'توضیحات', null=True, blank=True)
    cooperation_type = models.CharField(verbose_name=u'نوع همکاری', max_length=150)
    exit_reason = models.CharField(verbose_name=u'دلیل قطع همکاری', max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.title + " در " + self.place + "از تاریخ " + str(self.from_date) + " تا " + str(self.to_date)


class Skill(models.Model):
    class Meta:
        verbose_name = u'مهارت'
        verbose_name_plural = u'مهارت‌ها'

    title = models.CharField(max_length=150, verbose_name=u'عنوان')
    level = models.CharField(max_length=100, verbose_name=u'سطح تسلط')
    description = models.CharField(max_length=250, verbose_name=u'توضیح', null=True, blank=True)

    def __unicode__(self):
        return " - ".join([self.title, self.level])


class Resume(models.Model):
    class Meta:
        verbose_name = u'رزومه'
        verbose_name_plural = u'رزومه‌ها'

    resume_file = models.FileField(verbose_name=u'فایل رزومه', null=True, blank=True,
                                   upload_to=settings.MEDIA_ROOT + "user_resume")
    about_me = models.TextField(verbose_name=u'درباره من', null=True, blank=True)
    download_count = models.IntegerField(verbose_name=u'دفعات بارگیری', default=0)

    education = models.ManyToManyField(Education, verbose_name=u'تحصیلات')
    skill = models.ManyToManyField(Skill, related_name='skills', verbose_name=u'مهارت‌ها')
    experience = models.ManyToManyField(Experience, related_name='experiences', verbose_name=u'سوابق کاری')

    def __unicode__(self):
        return self.resume


class TemporaryLink(models.Model):
    class Meta:
        verbose_name = u'لینک موقت'
        verbose_name_plural = u'لینک های موقت'


    url_hash = models.CharField(u'لینک', max_length=120, unique=True)
    expire_date = models.DateTimeField(u'زمان ابطال')
    email = models.EmailField(u'پست الکترونیکی')

    def __unicode__(self):
        return self.email + str(self.expire_date.date())


class HomeDetails(models.Model):
    class Meta:
        verbose_name = u'متن صفحه اول'
        verbose_name_plural = u'متون صفحه اول'

    state = models.BooleanField(default=False, verbose_name=u'وضعیت')
    text1 = models.TextField(verbose_name=u'متن شماره یک')
    text2 = models.TextField(verbose_name=u'متن شماره دو')
    text3 = models.TextField(verbose_name=u'متن شماره سه')
    text4 = models.TextField(verbose_name=u'متن شماره چهار')
    text5 = models.TextField(verbose_name=u'متن شماره پنج')
