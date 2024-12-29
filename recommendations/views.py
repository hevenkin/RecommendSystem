from django.shortcuts import render, redirect

# Create your views here.
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .utils import (
    recommend_by_collaborative_filtering,
    recommend_by_contents,
    recommend_by_tags,
    recommend_by_svd,
    generate_reason_count_plot,
    generate_rating_histogram,
    generate_top_companies_plot
)
from django.template.loader import render_to_string
from recommendations.models import Drug
import base64

@login_required
def plot_view(request, plot_type):
    # 根据图表类型生成对应的图像缓冲区
    if plot_type == 'reason_count':
        buffer = generate_reason_count_plot()
    elif plot_type == 'rating_histogram':
        buffer = generate_rating_histogram()
    elif plot_type == 'top_companies':
        buffer = generate_top_companies_plot()
    else:
        return HttpResponse("无效图像类型！", content_type='text/plain')

    # 将图像缓冲区转换为 base64 编码
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    # 渲染 HTML 内容，返回图像
    html_content = render_to_string('recommendations/plot_image.html', {'image_base64': image_base64})
    return HttpResponse(html_content)

@login_required
def plot_home(request):
    # 渲染模板页面
    return render(request, 'recommendations/plot_home.html')

@login_required
def recommendation_home(request):
    if request.method == 'POST':
        drug_name = request.POST.get('drug_name')
        recommend_type = request.POST.get('recommend_type')

        # 检查用户是否输入了药品名和推荐类型
        if not drug_name or not recommend_type:
            return JsonResponse({'error': '请输入药品名并选择推荐系统类型。'})

        # 验证药品是否存在于数据库
        drug_exists = Drug.objects.filter(name=drug_name).exists()
        if not drug_exists:
            return JsonResponse({'error': f'药品名 "{drug_name}" 不存在，请重新输入！'}, status=400)

        if recommend_type == 'collaborative':
            recommendations = recommend_by_collaborative_filtering(drug_name)
        elif recommend_type == 'content':
            recommendations = recommend_by_contents(drug_name)
        elif recommend_type == 'tag':
            recommendations = recommend_by_tags(drug_name)
        elif recommend_type == 'latent':
            recommendations = recommend_by_svd(drug_name)
        else:
            recommendations = []

        # 确保返回的数据是列表
        if isinstance(recommendations, pd.Series):
            recommendations = recommendations.tolist()

        return JsonResponse({'recommendations': recommendations})

    return render(request, 'recommendations/recommendation_home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')  # 获取原始请求的目标URL
            return redirect(next_url if next_url else 'recommendation_home')  # 登录成功后跳转到主页
        else:
            return render(request, 'recommendations/login.html', {'error': '用户名或密码错误！'})
    return render(request, 'recommendations/login.html')