from unittest.mock import MagicMock, patch

import pytest
from agents.base_agent import BaseAgent


# Concrete implementation for testing
class MockAgent(BaseAgent):
    def get_capabilities(self):
        return {"test": "capability"}


@pytest.fixture
def mock_genai():
    with patch("agents.base_agent.genai") as mock:
        # Mock the model behavior
        mock_model = MagicMock()
        mock.GenerativeModel.return_value = mock_model

        # Async mock for generate_content_async
        async def async_response(*args, **kwargs):
            response = MagicMock()
            response.text = "Mocked response"
            return response

        mock_model.generate_content_async.side_effect = async_response
        yield mock


@pytest.fixture
def agent(mock_genai):
    return MockAgent(name="Tester", role="Testing", system_prompt="You are a test.")


def test_agent_initialization(agent):
    assert agent.name == "Tester"
    assert agent.role == "Testing"
    assert len(agent.history) == 0


@pytest.mark.asyncio
async def test_agent_execute(agent, mock_genai):
    result = await agent.execute("Test task")
    assert result == "Mocked response"
    assert len(agent.history) == 1
    assert agent.history[0]["task"] == "Test task"
    assert agent.history[0]["result"] == "Mocked response"
