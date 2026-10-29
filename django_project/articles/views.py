from django.views.generic import ListView, DetailView, FormView 
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView 
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from django.views import View
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)
    def get_success_url(self):
        article = self.object
        return reverse("article_detail", kwargs={"pk": article.pk})

class CommentGet(DetailView):
    model = Article
    template_name = "article_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context



class ArticleListView(LoginRequiredMixin, ListView): 
    model = Article
    template_name = "article_list.html"
class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user
            comment.save()
            return redirect("article_detail", self.object.pk)

        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Article
    fields = (
    "title",
    "body",
    )
    template_name = "article_edit.html"
    def test_func(self): 
        obj = self.get_object()
        return obj.author == self.request.user
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "article_new.html"
    fields = ("title", "body",)
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
