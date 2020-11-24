
from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
      path('log', views.log),
       path('books', views.books),
        path('logout', views.logout),
          path('addbook', views.addbook),
           path('books/<str:id>', views.edit),
            
             path('update/<str:id>', views.update),
             path('books/delete/<str:id>', views.delete),
              path('favorite/<str:id>', views.favorite),
              path('unfavoriet/<str:id>', views.unfavoriet),

]


  
