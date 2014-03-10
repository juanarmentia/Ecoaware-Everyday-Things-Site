from django.db import models

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

COUNTRY_CHOICES = (
    ("","Country..."),
    ("AF","Afghanistan"),
    ("AL","Albania"),
    ("DZ","Algeria"),
    ("AS","American Samoa"),
    ("AD","Andorra"),
    ("AG","Angola"),
    ("AI","Anguilla"),
    ("AG","Antigua &amp; Barbuda"),
    ("AR","Argentina"),
    ("AA","Armenia"),
    ("AW","Aruba"),
    ("AU","Australia"),
    ("AT","Austria"),
    ("AZ","Azerbaijan"),
    ("BS","Bahamas"),
    ("BH","Bahrain"),
    ("BD","Bangladesh"),
    ("BB","Barbados"),
    ("BY","Belarus"),
    ("BE","Belgium"),
    ("BZ","Belize"),
    ("BJ","Benin"),
    ("BM","Bermuda"),
    ("BT","Bhutan"),
    ("BO","Bolivia"),
    ("BL","Bonaire"),
    ("BA","Bosnia &amp; Herzegovina"),
    ("BW","Botswana"),
    ("BR","Brazil"),
    ("BC","British Indian Ocean Ter"),
    ("BN","Brunei"),
    ("BG","Bulgaria"),
    ("BF","Burkina Faso"),
    ("BI","Burundi"),
    ("KH","Cambodia"),
    ("CM","Cameroon"),
    ("CA","Canada"),
    ("IC","Canary Islands"),
    ("CV","Cape Verde"),
    ("KY","Cayman Islands"),
    ("CF","Central African Republic"),
    ("TD","Chad"),
    ("CD","Channel Islands"),
    ("CL","Chile"),
    ("CN","China"),
    ("CI","Christmas Island"),
    ("CS","Cocos Island"),
    ("CO","Colombia"),
    ("CC","Comoros"),
    ("CG","Congo"),
    ("CK","Cook Islands"),
    ("CR","Costa Rica"),
    ("CT","Cote D'Ivoire"),
    ("HR","Croatia"),
    ("CU","Cuba"),
    ("CB","Curacao"),
    ("CY","Cyprus"),
    ("CZ","Czech Republic"),
    ("DK","Denmark"),
    ("DJ","Djibouti"),
    ("DM","Dominica"),
    ("DO","Dominican Republic"),
    ("TM","East Timor"),
    ("EC","Ecuador"),
    ("EG","Egypt"),
    ("SV","El Salvador"),
    ("GQ","Equatorial Guinea"),
    ("ER","Eritrea"),
    ("EE","Estonia"),
    ("ET","Ethiopia"),
    ("FA","Falkland Islands"),
    ("FO","Faroe Islands"),
    ("FJ","Fiji"),
    ("FI","Finland"),
    ("FR","France"),
    ("GF","French Guiana"),
    ("PF","French Polynesia"),
    ("FS","French Southern Ter"),
    ("GA","Gabon"),
    ("GM","Gambia"),
    ("GE","Georgia"),
    ("DE","Germany"),
    ("GH","Ghana"),
    ("GI","Gibraltar"),
    ("GB","Great Britain"),
    ("GR","Greece"),
    ("GL","Greenland"),
    ("GD","Grenada"),
    ("GP","Guadeloupe"),
    ("GU","Guam"),
    ("GT","Guatemala"),
    ("GN","Guinea"),
    ("GY","Guyana"),
    ("HT","Haiti"),
    ("HW","Hawaii"),
    ("HN","Honduras"),
    ("HK","Hong Kong"),
    ("HU","Hungary"),
    ("IS","Iceland"),
    ("IN","India"),
    ("ID","Indonesia"),
    ("IA","Iran"),
    ("IQ","Iraq"),
    ("IR","Ireland"),
    ("IM","Isle of Man"),
    ("IL","Israel"),
    ("IT","Italy"),
    ("JM","Jamaica"),
    ("JP","Japan"),
    ("JO","Jordan"),
    ("KZ","Kazakhstan"),
    ("KE","Kenya"),
    ("KI","Kiribati"),
    ("NK","Korea North"),
    ("KS","Korea South"),
    ("KW","Kuwait"),
    ("KG","Kyrgyzstan"),
    ("LA","Laos"),
    ("LV","Latvia"),
    ("LB","Lebanon"),
    ("LS","Lesotho"),
    ("LR","Liberia"),
    ("LY","Libya"),
    ("LI","Liechtenstein"),
    ("LT","Lithuania"),
    ("LU","Luxembourg"),
    ("MO","Macau"),
    ("MK","Macedonia"),
    ("MG","Madagascar"),
    ("MY","Malaysia"),
    ("MW","Malawi"),
    ("MV","Maldives"),
    ("ML","Mali"),
    ("MT","Malta"),
    ("MH","Marshall Islands"),
    ("MQ","Martinique"),
    ("MR","Mauritania"),
    ("MU","Mauritius"),
    ("ME","Mayotte"),
    ("MX","Mexico"),
    ("MI","Midway Islands"),
    ("MD","Moldova"),
    ("MC","Monaco"),
    ("MN","Mongolia"),
    ("MS","Montserrat"),
    ("MA","Morocco"),
    ("MZ","Mozambique"),
    ("MM","Myanmar"),
    ("NA","Nambia"),
    ("NU","Nauru"),
    ("NP","Nepal"),
    ("AN","Netherland Antilles"),
    ("NL","Netherlands (Holland, Europe)"),
    ("NV","Nevis"),
    ("NC","New Caledonia"),
    ("NZ","New Zealand"),
    ("NI","Nicaragua"),
    ("NE","Niger"),
    ("NG","Nigeria"),
    ("NW","Niue"),
    ("NF","Norfolk Island"),
    ("NO","Norway"),
    ("OM","Oman"),
    ("PK","Pakistan"),
    ("PW","Palau Island"),
    ("PS","Palestine"),
    ("PA","Panama"),
    ("PG","Papua New Guinea"),
    ("PY","Paraguay"),
    ("PE","Peru"),
    ("PH","Philippines"),
    ("PO","Pitcairn Island"),
    ("PL","Poland"),
    ("PT","Portugal"),
    ("PR","Puerto Rico"),
    ("QA","Qatar"),
    ("ME","Republic of Montenegro"),
    ("RS","Republic of Serbia"),
    ("RE","Reunion"),
    ("RO","Romania"),
    ("RU","Russia"),
    ("RW","Rwanda"),
    ("NT","St Barthelemy"),
    ("EU","St Eustatius"),
    ("HE","St Helena"),
    ("KN","St Kitts-Nevis"),
    ("LC","St Lucia"),
    ("MB","St Maarten"),
    ("PM","St Pierre &amp; Miquelon"),
    ("VC","St Vincent &amp; Grenadines"),
    ("SP","Saipan"),
    ("SO","Samoa"),
    ("AS","Samoa American"),
    ("SM","San Marino"),
    ("ST","Sao Tome &amp; Principe"),
    ("SA","Saudi Arabia"),
    ("SN","Senegal"),
    ("RS","Serbia"),
    ("SC","Seychelles"),
    ("SL","Sierra Leone"),
    ("SG","Singapore"),
    ("SK","Slovakia"),
    ("SI","Slovenia"),
    ("SB","Solomon Islands"),
    ("OI","Somalia"),
    ("ZA","South Africa"),
    ("ES","Spain"),
    ("LK","Sri Lanka"),
    ("SD","Sudan"),
    ("SR","Suriname"),
    ("SZ","Swaziland"),
    ("SE","Sweden"),
    ("CH","Switzerland"),
    ("SY","Syria"),
    ("TA","Tahiti"),
    ("TW","Taiwan"),
    ("TJ","Tajikistan"),
    ("TZ","Tanzania"),
    ("TH","Thailand"),
    ("TG","Togo"),
    ("TK","Tokelau"),
    ("TO","Tonga"),
    ("TT","Trinidad &amp; Tobago"),
    ("TN","Tunisia"),
    ("TR","Turkey"),
    ("TU","Turkmenistan"),
    ("TC","Turks &amp; Caicos Is"),
    ("TV","Tuvalu"),
    ("UG","Uganda"),
    ("UA","Ukraine"),
    ("AE","United Arab Emirates"),
    ("GB","United Kingdom"),
    ("US","United States of America"),
    ("UY","Uruguay"),
    ("UZ","Uzbekistan"),
    ("VU","Vanuatu"),
    ("VS","Vatican City State"),
    ("VE","Venezuela"),
    ("VN","Vietnam"),
    ("VB","Virgin Islands (Brit)"),
    ("VA","Virgin Islands (USA)"),
    ("WK","Wake Island"),
    ("WF","Wallis &amp; Futana Is"),
    ("YE","Yemen"),
    ("ZR","Zaire"),
    ("ZM","Zambia"),
    ("ZW","Zimbabwe"),
)

#FIELD_CHOICES = (
#    ("IT","Information Technology"),
#    ("CS","Computer Science"),
#)

#PERIOD_CHOICES = (
#    ("AM","AM"),
#    ("PM","PM"),
#)
#
#HR_CHOICES = (
#    (0,"00"),
#    (1,"01"),
#    (2,"02"),
#    (3,"03"),
#    (4,"04"),
#    (5,"05"),
#    (6,"06"),
#    (7,"07"),
#    (8,"08"),
#    (9,"09"),
#    (10,"10"),
#    (11,"11"),
#    (12,"12"),
#)
#
#MIN_CHOICES = (
#    (0,"00"),
#    (5,"05"),
#    (10,"10"),
#    (15,"15"),
#    (20,"20"),
#    (25,"25"),
#    (30,"30"),
#    (35,"35"),
#    (40,"40"),
#    (45,"45"),
#    (50,"50"),
#    (55,"55"),
#)



    

class DevelopedActivity(models.Model):
    idDevActivity = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    
    def __unicode__(self):
        return self.name
    
    
class DeviceCategory(models.Model):
    idCategory = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=45)
    
    def __unicode__(self):
        return self.name
    
class FieldActivity(models.Model):
    idFieldActivity = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    acronym = models.CharField(max_length=2)
    
    def __unicode__(self):
        return self.name
    

class Device(models.Model):
    username = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=20)
    category = models.ForeignKey(DeviceCategory)
    email = models.EmailField()
    devActivity = models.ForeignKey(DevelopedActivity)
    fieldactivity = models.ManyToManyField(FieldActivity)
    country =  models.CharField(
        max_length=50,
        choices=COUNTRY_CHOICES,
        blank=False,
        null=False,
    )
    region = models.CharField(max_length=11, null=True)
    city = models.CharField(max_length=15)
    startSch = models.TimeField()
    finishSch = models.TimeField()
    
    def __unicode__(self):
        return self.name
        

# Create your models here.
class TagRFID(models.Model):
    rfid = models.CharField(primary_key=True, max_length=10)
    active = models.BooleanField()
    device = models.ForeignKey(Device)
    
    def __unicode__(self):
        return self.rfid

class CustomUser(models.Model):
    user = models.OneToOneField(User)
    rfid = models.CharField(max_length=8)
    twitter = models.CharField(max_length=15, blank=True)
    
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
    
  
class Question(models.Model):
    idQuestion = models.AutoField(primary_key=True)
    question = models.CharField(max_length=245)
    module = models.IntegerField()
    
    def __unicode__(self):
        return self.question


class User_Question(models.Model):
    rfid = models.ForeignKey(TagRFID)
    question = models.ForeignKey(Question)
    answer = models.PositiveSmallIntegerField()

    
#class Fields_Devices(models.Model):
#    device = models.ForeignKey(Device)
#    field = models.ForeignKey(FieldActivity)

class Counter(models.Model):
    idCounter = models.AutoField(primary_key=True)
    username = models.CharField(max_length=15)
    date = models.DateField()
    