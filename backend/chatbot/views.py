from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid

from .models import ChatHistory
from .services import get_ai_chat_response

def get_or_create_session_id(request):
    session_id = request.session.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['chat_session_id'] = session_id
    return session_id


@login_required
def chatbot_page(request):
    """Full-page dedicated AI Pet Care Assistant."""
    session_id = get_or_create_session_id(request)
    
    if request.user.is_authenticated:
        history = ChatHistory.objects.filter(user=request.user).order_by('created_at')[:20]
    else:
        history = ChatHistory.objects.filter(session_id=session_id).order_by('created_at')[:20]

    initial_query = request.GET.get('q', '')

    context = {
        'history': history,
        'initial_query': initial_query,
    }
    return render(request, 'chatbot/chatbot_page.html', context)


@csrf_exempt
def chat_api(request):
    """
    JSON API endpoint used by both the global floating widget and the full chatbot page.
    Accepts POST with {'message': 'user question'}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        if request.content_type == 'application/json':
            body = json.loads(request.body.decode('utf-8'))
            query_text = body.get('message', '').strip()
        else:
            query_text = request.POST.get('message', '').strip()
    except Exception:
        query_text = request.POST.get('message', '').strip()

    if not query_text:
        return JsonResponse({'error': 'Empty message received'}, status=400)

    session_id = get_or_create_session_id(request)
    user = request.user if request.user.is_authenticated else None

    result = get_ai_chat_response(query_text, user=user, session_id=session_id)

    if isinstance(result, dict):
        resp_text = result.get('response', '')
        model_name = result.get('model', 'PawPal AI')
        redirect_url = result.get('redirect_url', None)
        destination = result.get('destination', None)
        action = result.get('action', None)
    else:
        resp_text = str(result)
        model_name = 'PawPal AI'
        redirect_url = None
        destination = None
        action = None

    return JsonResponse({
        'status': 'success',
        'query': query_text,
        'response': resp_text,
        'model': model_name,
        'redirect_url': redirect_url,
        'destination': destination,
        'action': action,
    })


def chat_history_api(request):
    """Returns recent chat history for floating widget initialization."""
    session_id = get_or_create_session_id(request)
    if request.user.is_authenticated:
        history = ChatHistory.objects.filter(user=request.user).order_by('created_at')[:15]
    else:
        history = ChatHistory.objects.filter(session_id=session_id).order_by('created_at')[:15]

    data = [{
        'query': h.user_query,
        'response': h.bot_response,
        'created_at': h.created_at.strftime('%H:%M'),
    } for h in history]

    return JsonResponse({'history': data})


@csrf_exempt
def clear_chat_api(request):
    """Clears conversation history for the current user/session."""
    session_id = get_or_create_session_id(request)
    if request.user.is_authenticated:
        ChatHistory.objects.filter(user=request.user).delete()
    else:
        ChatHistory.objects.filter(session_id=session_id).delete()
    return JsonResponse({'status': 'cleared'})
