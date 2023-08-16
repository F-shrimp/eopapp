from django.db import models

class App_Info1(models.Model):
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
