from django.contrib import admin

# Register your models here.


from .models import Studentinfo
from .models import Studcontact
from .models import Studemail
from .models import Profinfo
from .models import Profemail
from .models import Profcontact
from .models import Projprofcom
from .models import Profidea
from .models import FilesUpload
from .models import Project
from .models import Domains
from .models import Projdom
from .models import Projprof
from .models import Studprojgrade

admin.site.register(Studentinfo)
admin.site.register(Studcontact)
admin.site.register(Studemail)
admin.site.register(Profinfo)
admin.site.register(Profemail)
admin.site.register(Profcontact)
admin.site.register(Projprofcom)
admin.site.register(Profidea)
admin.site.register(FilesUpload)
admin.site.register(Project)
admin.site.register(Domains)
admin.site.register(Projdom)
admin.site.register(Projprof)
admin.site.register(Studprojgrade)