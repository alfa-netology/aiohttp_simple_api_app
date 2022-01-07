from application import app, web
import application.views as views

app.add_routes([web.get('/status', views.StatusView)])

app.add_routes([web.get('/users_list', views.AdvertisingListView)])
app.add_routes([web.get('/advertisings_list', views.UserListView)])

app.add_routes([web.post('/user', views.UserView)])
app.add_routes([web.get('/user/{user_id}', views.UserView)])

app.add_routes([web.post('/advertising', views.AdvertisingView)])
app.add_routes([web.get('/advertising/{id}', views.AdvertisingView)])
app.add_routes([web.patch('/advertising/{id}', views.AdvertisingView)])
app.add_routes([web.delete('/advertising/{id}', views.AdvertisingView)])
