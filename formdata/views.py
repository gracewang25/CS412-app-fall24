from django.shortcuts import render, redirect

# Create your views here.
def show_form(request):
    '''show the html form to the client'''

    template_name = 'formdata/form.html'
    return render(request, template_name)

def submit(request):
    '''handle form submition, read out data, generate a response'''

    template_name = "formdata/confirmation.html"
    print(request)

    # check for POST request
    if request.POST:
        
        # read form data into python variables:
        name = request.POST['name']
        fav_color = request.POST['fav_color']

        # read values from the Post request -> packaged to use in the respons:
        context = {
            'name': name,
            'fav_color': fav_color,
        }

    # generate the response and pass context variables to the html
        return render(request, template_name, context)


# # this is the 'best solution': redirect to the correct url
#     return redirect(request, "")
                        
