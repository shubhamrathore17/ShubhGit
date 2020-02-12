







{% extends 'base.html' %}






{% block content %}
  <h2>Welcome, {{ user.get_full_name }} <small>{{ user.username }}</small>!</h2>
  <p>Your email address: {{ user.email }}</p>
  <p>ROLE: {{user.profile.role}} </p>
  <p>BIRTH DATE: {{user.profile.birth_date}} </p>
  <p>
  <p>GENDER: {{user.profile.gender}} </p>
  {# <p>profile pic:<br><img src="{{user.profile.profile_pic.url}}"></p> #}
  
{% endblock %}




# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()
<!DOCTYPE html>
<html>
<head>
  <title></title>

<style>
  .helptext{
    visibility: hidden;
}
</style>
</head>
<body>
  <form method="post">
      {% csrf_token %}
      {{ form }}
      <button type="submit">Save changes</button>
  </form>
</body>
</html>




    def get_success_url(self, **kwargs):
        return ('/artical/'+str(self.kwargs['pk'])+'/') 
       



    class PropertyUpdateView(UpdateView):
    model = Property
    form_class = PropertyUpdateForm
    template_name = "property_update_form.html"
    # success_url = reverse_lazy('property_detail')
    def get_success_url(self, **kwargs):
        return ('/artical/'+str(self.kwargs['pk'])+'/') 


    class PropertyUpdateForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('user', 'title', 'property_pic' ,'description' ,'address', 'price' ,'sqft')
       
      path('edit_property/<int:pk>/',views.PropertyUpdateView.as_view(), name='edit_property'),


      <form method="post">{% csrf_token %}
          {{ form.as_p }}
          <input type="submit" value="Update">
      </form>




      if profile.role == 'Propertyowner':
            return render(request, 'profile_page.html', {'properties':properties ,'profile':profile})
        else:
            return render(request, 'profile_page_rental.html', {'properties':properties ,'profile':profile})





  
@login_required(login_url='/login/')
def apply_for_property(request,property_id):
    if request.method == "POST":
        import pdb; pdb.set_trace()
        property = Property.objects.get(pk=property_id)
        property_title=property.title
        owner_email=property.user.email
        applier_contact_no=request.user.profile.phone
        body = "Hey, i am interested in your property.  "+property_title+ "contact me over here"+applier_contact_no+" "
        send_mail = EmailMessage("APPLIED",body,settings.FROM_EMAIL,to=[owner_email])
        send_mail.send()
        messages.success(request, 'Applied successfully')
        return HttpResponseRedirect('/home/')













            <span class="progress-bar" style="width: 26.85%;"></span




            ASASR1245D


  role_choices=(
('male' ,male),
    )