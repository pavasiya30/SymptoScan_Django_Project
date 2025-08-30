from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Prediction, AIChatLog
from .ai_chat_service import ai_chat_service
import json

@login_required
def chat_with_ai(request, prediction_id):
    """Main chat interface - only accessible after prediction"""
    prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)
    
    # Get conversation ID from session or query parameter
    conversation_id = request.GET.get('conversation_id') or request.session.get(f'conversation_id_{prediction_id}')
    if not conversation_id:
        conversation_id = ai_chat_service.generate_conversation_id()
    
    # Get chat history
    chat_history = AIChatLog.objects.filter(
        user=request.user,
        conversation_id=conversation_id
    ).order_by('timestamp')
    
    # Check if this is the first time accessing chat for this prediction
    is_first_access = not AIChatLog.objects.filter(
        user=request.user,
        prediction=prediction,
        conversation_id=conversation_id
    ).exists()
    
    context = {
        'prediction': prediction,
        'conversation_id': conversation_id,
        'chat_history': chat_history,
        'is_first_access': is_first_access,
    }
    
    return render(request, 'chat_interface.html', context)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Handle sending messages to AI"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        prediction_id = data.get('prediction_id')
        conversation_id = data.get('conversation_id')
        
        if not message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get prediction
        prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)
        
        # Generate AI response
        result = ai_chat_service.generate_response(
            user=request.user,
            message=message,
            prediction=prediction,
            conversation_id=conversation_id
        )
        
        return JsonResponse({
            'response': result['response'],
            'conversation_id': result['conversation_id'],
            'is_health_related': result.get('is_health_related', True),
            'success': True
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'An error occurred while processing your message',
            'details': str(e)
        }, status=500)

@login_required
def start_new_conversation(request, prediction_id):
    """Start a new conversation for a prediction"""
    prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)
    
    # Generate new conversation ID
    conversation_id = ai_chat_service.generate_conversation_id()
    
    # Create initial AI message
    initial_message = ai_chat_service.create_initial_context_message(prediction)
    
    # Save initial message
    AIChatLog.objects.create(
        user=request.user,
        disease=prediction.disease,
        prediction=prediction,
        conversation_id=conversation_id,
        message="",
        response=initial_message,
        is_user_message=False
    )
    
    # Store conversation_id in session for the chat interface
    request.session[f'conversation_id_{prediction_id}'] = conversation_id
    
    # Redirect to chat interface
    return redirect('chat_with_ai', prediction_id=prediction_id)

@login_required
def chat_history(request):
    """View all chat conversations for the user"""
    conversations = AIChatLog.objects.filter(
        user=request.user
    ).values('conversation_id', 'disease__name', 'prediction__risk_level', 'timestamp').distinct()
    
    # Group by conversation
    chat_sessions = []
    for conv in conversations:
        if conv['conversation_id']:
            # Get the first message of this conversation
            first_message = AIChatLog.objects.filter(
                conversation_id=conv['conversation_id']
            ).order_by('timestamp').first()
            
            chat_sessions.append({
                'conversation_id': conv['conversation_id'],
                'disease_name': conv['disease__name'],
                'risk_level': conv['prediction__risk_level'],
                'timestamp': conv['timestamp'],
                'first_message': first_message.response if first_message and not first_message.is_user_message else "Conversation started"
            })
    
    context = {
        'chat_sessions': chat_sessions
    }
    
    return render(request, 'chat_history.html', context)

@login_required
def view_conversation(request, conversation_id):
    """View a specific conversation"""
    # Verify user owns this conversation
    chat_logs = AIChatLog.objects.filter(
        user=request.user,
        conversation_id=conversation_id
    ).order_by('timestamp')
    
    if not chat_logs.exists():
        messages.error(request, 'Conversation not found.')
        return redirect('chat_history')
    
    # Get prediction info
    prediction = chat_logs.first().prediction
    
    context = {
        'chat_history': chat_logs,
        'conversation_id': conversation_id,
        'prediction': prediction
    }
    
    return render(request, 'view_conversation.html', context)

@login_required
def delete_conversation(request, conversation_id):
    """Delete a conversation"""
    if request.method == 'POST':
        # Verify user owns this conversation
        chat_logs = AIChatLog.objects.filter(
            user=request.user,
            conversation_id=conversation_id
        )
        
        if chat_logs.exists():
            chat_logs.delete()
            messages.success(request, 'Conversation deleted successfully.')
        else:
            messages.error(request, 'Conversation not found.')
    
    return redirect('chat_history')
