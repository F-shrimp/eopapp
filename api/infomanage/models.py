from django.db import models

class App_Info(models.Model):
    aid = models.AutoField(primary_key=True)
    #autoincrement表示该主键是一个自增的主键
    appname = models.CharField(max_length=64, blank=False)
    app_domain = models.CharField(max_length=64, blank=False)
    app_Owner = models.CharField(max_length=11, blank=False)
    restart_any = models.CharField(max_length=11, blank=False)
    rapid_reduction = models.CharField(max_length=11, blank=False)
    rapid_expansion = models.CharField(max_length=11, blank=False)
    def __str__(self):
        return self.appname
    class Meta:
        db_table = "appinfo_mana"

class App_rapid_reduction(models.Model):
    aid = models.AutoField(primary_key=True)
    #autoincrement表示该主键是一个自增的主键
    appname = models.CharField(max_length=64, blank=False)
    offline_any = models.CharField(max_length=11, blank=False)
    stop_any = models.CharField(max_length=11, blank=False)
    logback = models.CharField(max_length=11, blank=False)
    off_special_content = models.TextField(blank=True)
    def __str__(self):
        return self.appname
    class Meta:
        db_table = "rapid_reduction"

class App_rapid_expansion(models.Model):
    aid = models.AutoField(primary_key=True)
    #autoincrement表示该主键是一个自增的主键
    appname = models.CharField(max_length=64, blank=False)
    once_init = models.CharField(max_length=11, blank=False)
    on_deploy = models.CharField(max_length=11, blank=False)
    start_any = models.CharField(max_length=11, blank=False)
    health_check = models.CharField(max_length=11, blank=False)
    online_any =  models.CharField(max_length=11, blank=False)
    on_special_content = models.TextField(blank=True)
    def __str__(self):
        return self.appname
    class Meta:
        db_table = "rapid_expansion"

# Create your models here.
