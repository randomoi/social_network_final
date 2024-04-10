from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import  View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from social.models import GalleryImageItem
from social.forms import GalleryImageSubmissionForm

# START - code was developed with the help of documentation and other external research, please see referenced links.

# handles image upload
# https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/#handling-uploaded-files-with-a-model
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#saving-objects
# https://docs.djangoproject.com/en/4.2/topics/http/views/#render
@login_required
def image_gallery_upload(request):
    if request.method == 'POST':
        gallery_form = GalleryImageSubmissionForm(request.POST, request.FILES)
        if gallery_form.is_valid():
            # saves form data 
            gallery_image_item = gallery_form.save(commit=False) 
            # links it to current user
            gallery_image_item.user = request.user
            # saves image 
            gallery_image_item.save() 
            # redirects to home page 
            return redirect('social-home') 
    else:
        gallery_form = GalleryImageSubmissionForm()
    return render(request, 'social/image_gallery_upload_form.html', {'form': gallery_form}) 

# handles rendering of image gallery upload form
# https://docs.djangoproject.com/en/4.2/topics/forms/#the-form-class
# https://docs.djangoproject.com/en/4.2/topics/http/views/#render
@login_required
def image_gallery_upload_form(request):
    gallery_form = GalleryImageSubmissionForm()  
    return render(request, 'social/image_gallery_upload_form.html', {'form': gallery_form})  

# handles displaying image gallery
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-specific-objects-with-get
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-objects
# https://docs.djangoproject.com/en/4.2/topics/http/views/#render
class ImageGalleryView(View):
    def get(self, request, pk, *args, **kwargs):
        # get user through pk
        user = get_object_or_404(User, pk=pk) 

        # get all gallery items for the user
        image_gallery_items = GalleryImageItem.objects.filter(user=user) 

        # verify of image gallery belongs to currently logged in user
        belongs_to_user_gallery = user == request.user

        context = {
            'user': user,
            'image_gallery_items': image_gallery_items,
            'belongs_to_user_gallery': belongs_to_user_gallery,
        }

        return render(request, 'social/image_gallery.html', context)  

# handles deletion of image from gallery
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-objects
# https://docs.djangoproject.com/en/4.2/topics/http/views/#http404
# https://docs.djangoproject.com/en/4.2/topics/forms/#the-view
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect
@login_required
def delete_image_from_gallery(request, item_id):
    try:
        # get the GalleryImageItem object by ID
        image_item = GalleryImageItem.objects.get(id=item_id) 
    except GalleryImageItem.DoesNotExist:
        raise Http404("Image does not exist.")  

    # verify if user owns image gallery item
    if image_item.user == request.user: 
        # if yes, delete it
        image_item.delete()  
        # redirect to the user's gallery
        return redirect('user-gallery', pk=request.user.pk)  
    else:
        # raise an error if user is not owner
        raise Http404("Sorry, you are not authorized to delete image. Must me the owner to delete.")  

# References
# https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/#handling-uploaded-files-with-a-model
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#saving-objects
# https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#redirect
# https://docs.djangoproject.com/en/4.2/topics/forms/#the-form-class
# https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/#uploading-multiple-files
# https://docs.djangoproject.com/en/4.2/topics/forms/#the-view
# https://docs.djangoproject.com/en/4.2/topics/http/views/#render
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-specific-objects-with-get
# https://docs.djangoproject.com/en/4.2/topics/db/queries/#retrieving-objects
# https://docs.djangoproject.com/en/4.2/topics/http/views/#http404
# https://docs.djangoproject.com/en/4.2/ref/models/querysets/#values
# https://docs.djangoproject.com/en/4.2/ref/request-response/#jsonresponse

# END - code was developed with the help of documentation and other external research, please see referenced links.