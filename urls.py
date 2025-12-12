
from django.contrib import admin
from django.urls import path, include
from verify.compare_face import views
from verify.compare_face import views as compare_face_views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('verify.urls')),
    path('compare_face/', include('verify.compare_face.urls')),
    path('compare_face/verify-live-face/', compare_face_views.compare_faces_with_images, name='verify_live_face'),
    path('compare-faces/', RedirectView.as_view(url='/compare_face/compare-faces/', permanent=True)), 

 ]
if settings.DEBUG:
    urlpatterns += static('/models/', document_root=settings.BASE_DIR / 'identity_verification' / 'verify' / 'static' / 'models')
