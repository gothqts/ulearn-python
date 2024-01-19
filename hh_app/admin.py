from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(PositionYearStat)
admin.site.register(CommonYearStat)
admin.site.register(CityStat)
admin.site.register(PositionCityStat)
admin.site.register(CommonSkillStat)
admin.site.register(PositionSkillStat)

admin.site.register(DemandGraph)
admin.site.register(GeographyGraph)
admin.site.register(SkillGraph)
