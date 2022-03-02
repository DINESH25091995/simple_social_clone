from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import forms
from . import models
from posts.models import Post#,likeMember

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
User = get_user_model()


class LikeView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("posts:single",kwargs={"slug": self.kwargs.get("slug")})
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post,slug=self.kwargs.get("slug"))
        try:
            likeMember.objects.create(user=self.request.user,post=post)
        except IntegrityError:
            messages.warning(self.request,("Warning, already liked this post {}".format(post.user)))
        else:
            messages.success(self.request,"You are now liked this post {} group.".format(post.user))
        return super().get(request, *args, **kwargs)

#def LikeView(request,pk):
#    post=get_object_or_404(Post,id=request.POST.get(post_id))
#    post.user_likes.add(request.user)
#    return HttpResponseRedirect(reverse('groups/single',args=[str(pk)]))

class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "group")


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','group')
    model = models.Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)



class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
