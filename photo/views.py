from django.shortcuts import render

# Create your views here.
# CRUDL - 이미지를 띄우는 방법
# 제네릭 뷰
# 쿼리셋 변경하기, context_data 추가하기, 권한 채크
# 함수형 뷰 <-> 클래스형 뷰

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Photo
# 뷰를 실행하기전에 특정한 로직을 추가로 실행하고 싶다면?
# 로그인 여부, csrf채크를 수행할 것이냐?
# 믹스인 : 클래스형 뷰
# 데코레이터 : 함수형 뷰       ---- 클래스형 뷰
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse

class PhotoList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_list.html'


class PhotoLikeList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def get_queryset(self):
        # 로그인한 유저가 좋아요를 클릭한 글을 찾아서 반환
        user = self.request.user
        queryset = user.like_post.all()
        return queryset

class PhotofavoriteList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def get_queryset(self):
        # 로그인한 유저가 북마크를 클릭한 글을 찾아서 반환
        user = self.request.user
        queryset = user.favorite_post.all()
        return queryset


from django.shortcuts import redirect
class PhotoCreate(CreateView):
    model = Photo
    fields = ['image','text']
    template_name = 'photo/photo_create.html'
    success_url = '/'

    def form_valid(self, form):
        # 입력된 자료가 올바른지 채크
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            # 올바르다면
            # form : 모델 폼
            form.instance.save()
            return redirect('/')
        else:
            # 올바르지 않다면
            return self.render_to_response({'form':form})

class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['image','text']
    template_name = 'photo/photo_update.html'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, "수정할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())

        return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)

class PhotoDelete(DeleteView):
    model = Photo
    template_name = 'photo/photo_delete.html'
    success_url = '/'

    # Life Cycle - iOS, Android, Vue, React, Djang, Rails
    # Framework 는 라이프 사이클이 존재 : 어떤 순서로 구동이 되느냐?
    # URLConf -> View -> Model 순으로
    # 어떤 뷰를 구동할 때 그 안에서 동작하는 순서

    # 사용자가 접속했을 때 get이냐? post? 등을 결정하고 분기하는 부분
    # def dispatch(self, request, *args, **kwargs):
    #     pass

    # 로직을 수행하고, 템플릿을 랜더링 한다.
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            # 삭제 페이지에서 권한이 없다!
            # 원래 디테일 페이지로 돌아가서 삭제에 실패했습니다.
            messages.warning(request, "삭제할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

    """
    def get(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        pass
    """

    # def get_object(self, queryset=None):
    #     # 해당 쿼리셋을 이용해서 현재 페이지에 필요한 object를 인스턴스화 한다.
    #     pass
    #
    # def get_queryset(self):
    #     # 어떻게 데이터를 가져올 것이냐?
    #     pass


class PhotoDetail(DetailView):
    model = Photo
    template_name = 'photo/photo_detail.html'


from django.views.generic.base import View
from django.http import HttpResponseForbidden

from urllib.parse import urlparse

class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        # like를 할 정보가 있다면 진행, 없다면 중단
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            # 1. 어떤 포스팅?
            # url : www.naver.com/blog/like/?photo_id=1
            # request.GET.get('photo_id')
            # url : www.naver.com/blog/like/1/
            # path('blog/like/<int:photo_id>/')
            # kwargs['photo_id']
            # 2. 누가?
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)
            # 레퍼러 얻기
            referer_url = request.META.get('HTTP_REFERER')
            # https://www.naver.com
            # /blog/doc/1234/
            # ?id=2223
            # domain, path, query
            # path
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)



class PhotoSave(View):
    def get(self, request, *args, **kwargs):
        # like를 할 정보가 있다면 진행, 없다면 중단
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            # 1. 어떤 포스팅?
            # url : www.naver.com/blog/like/?photo_id=1
            # request.GET.get('photo_id')
            # url : www.naver.com/blog/like/1/
            # path('blog/like/<int:photo_id>/')
            # kwargs['photo_id']
            # 2. 누가?
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.favorite.all():
                    photo.favorite.remove(user)
                else:
                    photo.favorite.add(user)
            # 레퍼러 얻기
            referer_url = request.META.get('HTTP_REFERER')
            # https://www.naver.com
            # /blog/doc/1234/
            # ?id=2223
            # domain, path, query
            # path
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)


################################################################


from rest_framework import generics
from .serializers import PhotoSerializer
from .models import Photo
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny


class PhotoView(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (AllowAny, )

class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    # renderer_classes = [JSONRenderer]

