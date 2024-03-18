
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from leads.views import landing_page, SignupView
from django.conf import settings
from leads import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path('', landing_page, name='landing-page'),
    path('leads/', include('leads.urls', namespace='leads')),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logoutUser, name='logout'),
    


]
 