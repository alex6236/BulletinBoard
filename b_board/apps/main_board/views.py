from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, render, redirect
from .models import Ad, Category, Reply, Subscription
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import AdCreateForm, AdUpdateForm, ReplyCreateForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
# =============================
from django.shortcuts import get_object_or_404
from django.views import View
# ======================

User = get_user_model()


class AdListView(ListView):
    model = Ad
    template_name = 'main_board/ad_list.html'
    context_object_name = 'ad_list'
    paginate_by = 3
    
    def get_queryset(self):
        return Ad.objects.filter(status='published').order_by('-time_create')
    
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_now'] = datetime.now(timezone.utc)
        context['title'] = 'Главная страница'
        return context
    
class DraftListView(ListView):
    model = Ad
    template_name = 'main_board/draft_list.html'
    context_object_name = 'draft_list'
    # queryset = Ad.objects.all().order_by('-id')
    paginate_by = 2
    
    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user, status='draft').order_by('-time_create')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Черновики'
        return context
    


class AdDetailView(DetailView):
    model = Ad
    template_name = 'main_board/ad_detail.html'
    context_object_name = 'ad_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['form'] = ReplyCreateForm
        context['replies'] = Reply.objects.filter(reply=self.object).order_by('-created_reply')
        request_likes = get_object_or_404(Ad, slug=self.kwargs['slug'])
        liked = False
        if request_likes.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['number_likes'] = request_likes.rating()
        context['ad_is_liked'] = liked
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.reply = self.object
            reply.author = request.user
            reply.save()
            return redirect('ad_detail', slug=self.object.slug)
        return self.render_to_response(self.get_context_data(form=form))
    


def ad_like_user(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    if ad.likes.filter(id=request.user.id).exists():
        ad.likes.remove(request.user)
    else:
        ad.likes.add(request.user)
    return redirect(ad.get_absolute_url())
    
    
    
class DraftDetailView(DetailView):
    model = Ad
    template_name = 'main_board/draft_detail.html'
    context_object_name = 'draft_detail'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Ad.objects.filter(status='draft')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context
    
class ReplyPublishView(LoginRequiredMixin, SuccessMessageMixin, View):
    model = Reply
    success_message = 'Сообщение добавлено'
    login_url = 'login'
    
    def post(self, request, pk):
        reply = get_object_or_404(Reply, pk=pk)
        reply.is_published = True
        reply.save()
        return redirect('ad_detail', slug=reply.reply.slug)

class ReplyDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):  
    model = Reply  
    context_object_name = 'reply_delete'  
    template_name = 'main_board/reply_delete.html'
    success_message = 'Сообщение удалено'

    def get_success_url(self):
        return reverse_lazy('ad_detail', kwargs={'slug': self.object.reply.slug})

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        context['title'] = f'Удаление сообщения: {self.object.reply.title}'  
        return context
    
# без шаблона    
class CategoryAdListView(ListView):
    model = Ad
    template_name = 'main_board/category.html'
    paginate_by = 3
    
    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = Category.objects.get(slug=category_slug)
        return category.ad_set.all().filter(status='published').order_by('-id') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        category = Category.objects.get(slug=category_slug)
        context['category'] = category
        return context
    

class AdCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ad
    template_name = 'main_board/ad_create.html'
    form_class = AdCreateForm
    # login_url = 'ad_list'
    success_message = 'Объявление добавлено'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление объявления на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        video_file = self.request.FILES.get('video')
        if video_file:
            form.instance.video.save(video_file.name, video_file)
        form.save()
        notification_of_new_ad(form.instance)
        return super().form_valid(form) 

def notification_of_new_ad(ad):
    category = ad.category_ad
    subscribers = Subscription.objects.filter(categories=category).select_related('user')
    
    for subscriber in subscribers:
        user = subscriber.user
        email = user.email
        ad_url = ad.get_absolute_url()
        html = render_to_string('mail/new_ad_subscribers.html', {'ad': ad, 'user': user, 'ad_url': ad_url})
        msg = EmailMultiAlternatives(
            subject='Новое объявление в категории',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
       
    
    
class AdUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ad
    form_class = AdUpdateForm
    template_name = 'main_board/ad_update.html'
    success_message = 'Ваше объявление обновлено'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление объявления: {self.object.title}'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        video_file = self.request.FILES.get('video')
        if video_file:
            self.object.video.save(video_file.name, video_file)
        self.object.save()
        return super().form_valid(form) 
    
    
class DraftUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ad
    form_class = AdUpdateForm
    template_name = 'main_board/draft_update.html'
    success_message = 'Ваш черновик обновлен'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление отзыва: {self.object.title}'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form) 
    
class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    context_object_name = 'ad_delete'
    template_name = 'main_board/ad_delete.html'
    success_url = reverse_lazy('ad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление объявления: {self.object.title}'
        return context
    
    
class DraftDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    context_object_name = 'draft_delete'
    template_name = 'main_board/draft_delete.html'
    success_url = reverse_lazy('draft_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление объявления: {self.object.title}'
        return context
    
class SearchHeaderView(ListView):
    model = Ad
    template_name = 'main_board/search_header.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        if q:  
            multiple_q = Q(
                Q(title__iregex=q) |
                Q(author__username__icontains=q) |
                Q(text_ad__iregex=q))
            results = Ad.objects.filter(multiple_q).order_by('-id')
            context['results'] = results
            paginator = Paginator(results, self.paginate_by)
            page_number = self.request.GET.get('page')
            context['results'] = paginator.get_page(page_number)
        return context
    
class AllAdAuthorView(ListView):
    model = Ad
    template_name = 'main_board/all_ad_author.html'
    context_object_name = 'ads'
    ordering = ['-time_create']
    
    def get_queryset(self):
        author_id = self.kwargs['author_id']
        return super().get_queryset().filter(author_id=author_id, status='published')

# без шаблона
class AuthorAdsListView(ListView):
    model = Ad
    template_name = 'main_board/ad_author.html'
    paginate_by = 3

    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user, status='published').order_by('-time_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ads = self.get_queryset()
        context['ads'] = ads
        return context


@login_required
def subscribe_category(request):
    if request.method == 'POST':
        user = request.user
        email = user.email
        subscribe_all = bool(request.POST.get('subscribe_all'))
        # categories = request.POST.getlist('categories')
        category_id_List = request.POST.getlist('categories')
        categories = Category.objects.filter(id__in=category_id_List)
        print(categories)
    
        
        subscription, created = Subscription.objects.get_or_create(user=user)
        if subscribe_all:
            categories = Category.objects.all()
            subscription.categories.set(categories)
        else:
            subscription.categories.set(categories)
        html = render_to_string('mail/subscribed.html',
            {'categories': categories, 'user': user,},)
        msg = EmailMultiAlternatives(
            subject=f'Подписка на новости',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email, ],
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
        messages.success(request, "Поздравляем вы успешно подписались на рассылку")
        return redirect('ad_list')
    return redirect('ad_list')    
   
   
@login_required
def unsubscribe_user(request):
    user = request.user
    subscription = get_object_or_404(Subscription, user=user)
    if subscription:
        subscription.delete()
        messages.success(request, "Вы отписались от рассылки")
    else:
        messages.success(request, "У Вас нет подписок")
    return redirect('ad_list') 

@login_required
def subscription_view(request):
    user = request.user
    categories = Category.objects.all()
    
    try:
        subscription = Subscription.objects.get(user=user)
    except Subscription.DoesNotExist:
        subscription = None

    return render(request, 'main_board/subscribe_list.html', {'categories': categories, 'user': user, 'subscription': subscription})

def popular_ads(request):
    start_date = timezone.now() - timedelta(weeks=1)
    popular_ads = Ad.objects.filter(time_create__gte=start_date, status='published').order_by('-rating')[:5]
    print(popular_ads)
    context = {'popular_ads': popular_ads}
    return render(request, 'main_board/popular_ads.html', context)

