from django.shortcuts import render
from .models import PokemonCard
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def List(request):
    cards = PokemonCard.objects.all()
    # 使用 serialize 將 QuerySet 序列化為 JSON 格式的數據
    cards_json = serialize('json', cards)
    return JsonResponse(cards_json, safe=False)

def showcard(request):
    query = request.GET.get('card_id')
    context = {
        'card_id': f"tw{query.zfill(8)}.png",  # 將搜索關鍵字傳遞到模板，以便於模板中顯示
    }
    return render(request, 'showcard.html', context)
    #return render(request, 'showcard.html')



def cardList(request):
    # 假設這是您希望選擇的卡片的id列表
    card_rules = ['F','G','H']
    query = request.GET.get('q')
    if query:
        # 使用 Q 物件組合所有欄位的模糊查詢
        results = PokemonCard.objects.filter(
            Q(card_name__icontains=query) |
            Q(evolve_marker__icontains=query) |
            Q(card_hp__icontains=query) |
            Q(Type__icontains=query) |
            Q(Weakness__icontains=query) |
            Q(Resistance__icontains=query) |
            Q(Escape__icontains=query) |
            Q(description__icontains=query) |
            Q(card_alpha__icontains=query) |
            Q(card_rule__icontains=query) |
            Q(card_number__icontains=query) |
            Q(web_url__icontains=query) |
            Q(web_id__icontains=query)
        ).filter(card_rule__in=card_rules).order_by('card_rule')
    else:
        results = PokemonCard.objects.filter(card_rule__in=card_rules).order_by('card_rule')  # 如果沒有查詢字串，返回所有卡片

    paginator = Paginator(results, 10)  # 每頁顯示10個物件
    page = request.GET.get('page')
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        # 如果頁碼不是整數，顯示第一頁
        cards = paginator.page(1)
    except EmptyPage:
        # 如果頁碼超過範圍，顯示最後一頁
        cards = paginator.page(paginator.num_pages)

    context = {
        'cards': cards,  # 將分頁對象傳遞到模板
        'query': query,  # 將搜索關鍵字傳遞到模板，以便於模板中顯示
    }
    return render(request, 'cardlist.html', context)
