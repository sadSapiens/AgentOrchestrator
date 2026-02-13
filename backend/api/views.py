import asyncio
import json
import logging

from asgiref.sync import async_to_sync, sync_to_async
from django.apps import apps
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AgentInfoSerializer, ChatRequestSerializer

# Get logger
logger = logging.getLogger(__name__)


def get_orchestrator():
    """Helper to get the global orchestrator instance"""
    return apps.get_app_config("api").orchestrator


@method_decorator(csrf_exempt, name="dispatch")
class AgentListView(APIView):
    """
    Get status of all agents
    """

    def get(self, request):
        orchestrator = get_orchestrator()
        if not orchestrator:
            return Response(
                {"error": "Orchestrator not initialized"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        agents = orchestrator.list_agents()

        # Map to frontend format
        agents_data = []
        for _, agent in agents.items():
            agents_data.append(
                {
                    "name": agent["name"],
                    "ver": "v1.0",  # Placeholder
                    "status": "Idle",  # Default
                    "role": agent["role"],
                    "color": "#4285F4",  # Default blue
                    "cpu": 0,
                    "mem": 0,
                }
            )

        serializer = AgentInfoSerializer(agents_data, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name="dispatch")
class ChatView(APIView):
    """
    Handle chat/orchestration requests
    """

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            prompt = data.get("prompt")
            file_context = data.get("file_context")
            mode = data.get("mode")
            api_keys = data.get("api_keys")

            orchestrator = get_orchestrator()

            try:
                # Dynamic configuration of credentials
                if api_keys:
                    if "gemini" in api_keys and api_keys["gemini"]:
                        import google.generativeai as genai

                        genai.configure(api_key=api_keys["gemini"])

                full_prompt = prompt
                if file_context:
                    full_prompt += f"\n\n[CONTEXT]:\n{file_context}"

                if mode == "Auto Orchestration":
                    # Use streaming response
                    async def event_stream():
                        try:
                            async for event in orchestrator.orchestrate_task_stream(
                                full_prompt
                            ):
                                yield f"data: {json.dumps(event)}\n\n"
                        except Exception as e:
                            logger.error(f"Stream error: {e}")
                            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

                    return StreamingHttpResponse(
                        event_stream(), content_type="text/event-stream"
                    )
                else:
                    # Single agent execution (legacy/simple)
                    agent = orchestrator.get_agent("researcher")
                    # Run async method synchronously for compatibility
                    response = async_to_sync(agent.execute)(full_prompt)
                    return Response({"final_result": response})

            except Exception as e:
                logger.error(f"Error processing chat request: {e}", exc_info=True)
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
