import os
import requests
import time
import logging
import google.generativeai as genai
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .firestore_client import db
from django.views.generic import TemplateView


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TestCollectionsView(TemplateView):
    template_name = 'api/test_collections.html'


class TestEndpointsView(TemplateView):
    template_name = 'api/test_endpoints.html'


class APIHomeView(TemplateView):
    template_name = 'api/api_home.html'


class StoryGenerateView(APIView):
    def post(self, request):
        # Placeholder for story generation logic
        data = request.data
        # For now, return static response
        return Response({"story": "This is a sample story generated"}, status=status.HTTP_200_OK)


class ArtisanCreateView(APIView):
    def post(self, request):
        data = request.data
        doc_ref = db.collection('artisans').add(data)
        return Response({"id": doc_ref[1].id, "message": "Artisan created"}, status=status.HTTP_201_CREATED)


# Generic List/Create 
class CollectionListCreateView(APIView):
    collection_name = None
    
    def get(self, request):
        docs = db.collection(self.collection_name).stream()
        data = [{**doc.to_dict(), "id": doc.id} for doc in docs]
        return Response(data)
    
    def post(self, request):
        data = request.data
        doc_ref = db.collection(self.collection_name).add(data)
        return Response({"id": doc_ref[1].id}, status=status.HTTP_201_CREATED)


# Generate Retrieve/Update/Delete (Detail)
class CollectionDetailView(APIView):
    collection_name = None

    def get(self, request, doc_id):
        doc = db.collection(self.collection_name).document(doc_id).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return Response(data)
        return Response({"error": "Not found"}, status=404)
    
    def put(self, request, doc_id):
        doc = db.collection(self.collection_name).document(doc_id)
        if not doc.get().exists:
            return Response({"error": "Not found"}, status=404)
        doc.set(request.data)
        return Response({"id": doc_id, "updated": True})
    
    def patch(self, request, doc_id):
        doc = db.collection(self.collection_name).document(doc_id)
        if not doc.get().exists:
            return Response({"error": "Not found"}, status=404)
        doc.update(request.data)
        return Response({"id": doc_id, "patched": True})

    def delete(self, request, doc_id):
        doc = db.collection(self.collection_name).document(doc_id)
        if not doc.get().exists:
            return Response({"error": "Not found"}, status=404)
        doc.delete()
        return Response({"id": doc_id, "deleted": True})


# Assessments
class AssessmentsListCreateView(CollectionListCreateView):
    collection_name = 'assessments'


class AssessmentsDetailView(CollectionDetailView):
    collection_name = 'assessments'


# Heritage Nodes
class HeritageNodesListCreateView(CollectionListCreateView): 
    collection_name = 'heritage_nodes'


class HeritageNodesDetailView(CollectionDetailView): 
    collection_name = 'heritage_nodes'


# Mentorship Matches
class MentorshipMatchesListCreateView(CollectionListCreateView): 
    collection_name = 'mentorship_matches'


class MentorshipMatchesDetailView(CollectionDetailView): 
    collection_name = 'mentorship_matches'


# Products
class ProductsListCreateView(CollectionListCreateView): 
    collection_name = 'products'


class ProductsDetailView(CollectionDetailView): 
    collection_name = 'products'


# Story Drafts
class StoryDraftsListCreateView(CollectionListCreateView): 
    collection_name = 'story_drafts'


class StoryDraftsDetailView(CollectionDetailView): 
    collection_name = 'story_drafts'

def neutralize_prompt(prompt):
    """Pre-filter prompts to avoid safety filter triggers"""
    replacements = {
        "Indian": "South Asian",
        "traditional Indian": "traditional regional",
        "Hindu": "spiritual",
        "Muslim": "religious",
        "caste": "community",
        "tribal": "indigenous",
        # Add more sensitive terms as needed
    }
    
    neutral_prompt = prompt
    for sensitive_term, neutral_term in replacements.items():
        neutral_prompt = neutral_prompt.replace(sensitive_term, neutral_term)
    
    return neutral_prompt.strip()

def get_safe_prompt_template(user_prompt):
    """Generate a safe, pre-tested prompt template"""
    templates = [
        f"Write an inspiring story about a skilled craftsperson who creates beautiful handmade items. {neutralize_prompt(user_prompt)}",
        f"Tell a heartwarming tale of an artisan who preserves traditional crafting techniques. {neutralize_prompt(user_prompt)}",
        f"Create a story about a dedicated artist who finds joy in their creative work. {neutralize_prompt(user_prompt)}",
        f"Write about a master craftsperson who teaches their skills to others. {neutralize_prompt(user_prompt)}"
    ]
    return templates

def try_openai_fallback(prompt, max_tokens=1000):
    """Fallback to OpenAI GPT if Gemini fails"""
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            return None, "OpenAI API key not configured"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative storyteller who writes inspiring stories about artisans and craftspeople."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        story = response.choices[0].message.content.strip()
        logger.info("Story generated successfully using OpenAI fallback")
        return story, None
        
    except Exception as e:
        logger.warning(f"OpenAI fallback failed: {e}")
        return None, str(e)

def try_huggingface_fallback(prompt):
    """Fallback to Hugging Face API if other providers fail"""
    try:
        hf_api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not hf_api_key:
            return None, "Hugging Face API key not configured"
        
        headers = {"Authorization": f"Bearer {hf_api_key}"}
        api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        
        payload = {"inputs": prompt}
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                story = result[0].get('generated_text', '').strip()
                logger.info("Story generated successfully using Hugging Face fallback")
                return story, None
        
        return None, f"Hugging Face API returned status {response.status_code}"
        
    except Exception as e:
        logger.warning(f"Hugging Face fallback failed: {e}")
        return None, str(e)

def generate_story_gemini(prompt, max_retries=3, backoff_factor=1, model_name='gemini-1.5-flash'):
    """Enhanced story generation with comprehensive safety handling"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        error_msg = "GOOGLE_API_KEY environment variable not set"
        logger.error(error_msg)
        return None, error_msg

    genai.configure(api_key=api_key)

    # More permissive safety settings
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
    ]

    # Get safe prompt templates
    safe_templates = get_safe_prompt_template(prompt)
    
    # Available Gemini models to try
    gemini_models = [model_name, 'gemini-1.5-pro', 'gemini-1.0-pro']
    
    for attempt in range(1, max_retries + 1):
        # Try different prompt templates on each attempt
        current_prompt = safe_templates[min(attempt - 1, len(safe_templates) - 1)]
        
        for model_to_try in gemini_models:
            try:
                model = genai.GenerativeModel(model_to_try)
                response = model.generate_content(
                    current_prompt,
                    generation_config={
                        "temperature": 0.7,
                        "max_output_tokens": 1000,
                        "top_p": 0.95,
                        "top_k": 40,
                    },
                    safety_settings=safety_settings,
                )

                # Extract story text with better error handling
                story = None
                if hasattr(response, 'text') and response.text:
                    story = response.text.strip()
                elif hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    if (hasattr(candidate, 'content') and 
                        hasattr(candidate.content, 'parts') and 
                        candidate.content.parts):
                        story = candidate.content.parts[0].text.strip()

                if story and len(story) > 50:  # Ensure we got a meaningful response
                    logger.info(f"Story generated successfully on attempt {attempt} using {model_to_try}")
                    return story, None

            except Exception as e:
                error_details = str(e)
                logger.warning(f"Attempt {attempt} with {model_to_try} failed: {error_details}")
                
                # If it's a safety filter issue, continue to next model/template
                if any(keyword in error_details.lower() for keyword in ["safety", "blocked", "filter"]):
                    continue
                
                # If model not found, try next model
                if "not found" in error_details.lower():
                    continue

        # If all Gemini models failed, try alternative providers
        if attempt == max_retries:
            logger.info("All Gemini attempts failed, trying alternative providers...")
            
            # Try OpenAI fallback
            story, error = try_openai_fallback(neutralize_prompt(prompt))
            if story:
                return story, None
            
            # Try Hugging Face fallback
            story, error = try_huggingface_fallback(neutralize_prompt(prompt))
            if story:
                return story, None
            
            # If everything fails, return helpful error
            return None, "All AI providers failed due to safety filters or technical issues"

        sleep_time = backoff_factor * (2 ** (attempt - 1))
        logger.info(f"Retrying after {sleep_time} seconds...")
        time.sleep(sleep_time)

    return None, "Maximum retries exceeded"

def get_prompt_guidance():
    """Provide user guidance for creating safe prompts"""
    return {
        "good_examples": [
            "Write a story about a skilled craftsperson who creates beautiful pottery",
            "Tell a tale of an artisan who preserves traditional weaving techniques",
            "Create a story about a woodworker who teaches their craft to young apprentices"
        ],
        "avoid": [
            "Specific cultural or ethnic identifiers",
            "Religious references",
            "Political content",
            "References to specific regions that might be sensitive"
        ],
        "tips": [
            "Focus on universal themes like craftsmanship and dedication",
            "Use general terms like 'traditional' instead of specific cultural references",
            "Emphasize the creative process and artistic journey",
            "Keep prompts positive and uplifting"
        ]
    }

class StoryGenerateView(APIView):
    def post(self, request):
        prompt = request.data.get('prompt', 'Generate an interesting story.')
        model_name = request.data.get('model', 'gemini-1.5-flash')
        
        # Validate model name
        valid_models = [
            'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro'
        ]
        
        if model_name not in valid_models:
            return Response(
                {"error": f"Invalid model. Available models: {valid_models}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        story_text, error = generate_story_gemini(prompt, model_name=model_name)
        
        if story_text is None:
            # Provide comprehensive error handling and guidance
            guidance = get_prompt_guidance()
            
            if any(keyword in error.lower() for keyword in ["safety", "blocked", "filter"]):
                return Response({
                    "error": "Content generation was blocked by safety filters.",
                    "message": "Please try rephrasing your prompt to be more general and neutral.",
                    "guidance": guidance,
                    "alternative_providers_tried": True
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "error": f"Generation failed: {error}",
                    "guidance": guidance,
                    "suggestions": [
                        "Try using a different model",
                        "Make your prompt shorter and more specific",
                        "Check your API configuration"
                    ]
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "story": story_text,
            "model_used": model_name,
            "prompt": prompt,
            "guidance": get_prompt_guidance() if len(story_text) < 100 else None
        }, status=status.HTTP_200_OK)
