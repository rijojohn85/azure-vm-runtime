import os
import pytest
import asyncio
import logging
from unittest.mock import AsyncMock, patch
from src.log_vm_report import send_report_to_slack

@pytest.mark.asyncio(loop_scope='function')
async def test_send_report_no_webhook(monkeypatch: pytest.MonkeyPatch,caplog: pytest.LogCaptureFixture)->None:
    """
    Test to validate the function when no slack webhook is set
    """
    #ensure that the slack webhook is not set
    monkeypatch.delenv("SLACK_WEBHOOK_URL", raising=False)

    #clear the previous logs
    caplog.clear()

    #call the function with an empty dictionary
    await send_report_to_slack({})

    #check that an error about missing webhook is logged
    assert "Slack Webhook URL not found, please enable it into the environment variables" in caplog.text



@pytest.mark.asyncio(loop_scope='function')
async def test_send_report_success(monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    """
    Test that send_report_to_slack logs success when the POST request returns status 200.
    """
    # Set the Slack webhook URL
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "https://dummy.slack-webhook.url")

    vm_dict = {
        "vm1": {
            "resource_group": "rg1",
            "status": "Powerstate/running",
            "running_time": "25:00:00"
        }
    }
    caplog.clear()
    # Set the log level so that INFO messages are captured
    caplog.set_level(logging.INFO)
    
    # Create a dummy response that simulates a successful HTTP call (status 200)
    dummy_response = AsyncMock()
    dummy_response.status = 200
    # Setup dummy_response as an async context manager
    dummy_response.__aenter__.return_value = dummy_response


    # Create a dummy session that returns our dummy_post_context for post()
    dummy_session = AsyncMock()
    dummy_session.__aenter__.return_value = dummy_session
    dummy_session.post.return_value = dummy_response

    # Patch aiohttp.ClientSession globally so that our function uses our dummy session
    with patch("aiohttp.ClientSession", return_value=dummy_session):
        await send_report_to_slack(vm_dict=vm_dict)
    

    # Check that the success message is in the logs
    assert "Report sent to slack successfully" in caplog.text



@pytest.mark.asyncio(loop_scope='function')
async def test_send_report_failure(monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    """
    Test that send_report_to_slack logs failure when the POST request returns status 500.
    """
    # Set the Slack webhook URL
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "https://dummy.slack-webhook.url")

    vm_dict = {
        "vm1": {
            "resource_group": "rg1",
            "status": "Powerstate/running",
            "running_time": "25:00:00"
        }
    }
    caplog.clear()
    # Set the log level so that INFO messages are captured
    caplog.set_level(logging.INFO)
    
    # Create a dummy response that simulates a successful HTTP call (status 200)
    dummy_response = AsyncMock()
    dummy_response.status = 500
    # Setup dummy_response as an async context manager
    dummy_response.__aenter__.return_value = dummy_response


    # Create a dummy session that returns our dummy_post_context for post()
    dummy_session = AsyncMock()
    dummy_session.__aenter__.return_value = dummy_session
    dummy_session.post.return_value = dummy_response

    # Patch aiohttp.ClientSession globally so that our function uses our dummy session
    with patch("aiohttp.ClientSession", return_value=dummy_session):
        await send_report_to_slack(vm_dict=vm_dict)
    
    # Check that the success message is in the logs
    assert "Error sending report to slack, status code: 500" in caplog.text



@pytest.mark.asyncio(loop_scope='function')
async def test_send_report_exception(monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    """
    Test that send_report_to_slack logs an exception when there is an internal server error.
    """
    # Set the Slack webhook URL
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "https://dummy.slack-webhook.url")

    vm_dict = {
        "vm1": {
            "resource_group": "rg1",
            "status": "Powerstate/running",
            "running_time": "25:00:00"
        }
    }
    caplog.clear()
    # Set the log level so that INFO messages are captured
    caplog.set_level(logging.INFO)

    dummy_session = AsyncMock()
    dummy_session.__aenter__.return_value = dummy_session
    dummy_session.post.side_effect = Exception("Text Exception")

    with patch("aiohttp.ClientSession", return_value=dummy_session):
        await send_report_to_slack(vm_dict=vm_dict)
    
    assert "Error sending report to slack: Text Exception"