from mediation_logs import llmhelper
from mediation_logs.util.json_handler import MediationJSONConfig

def test_sample_response():
    # Load the MediationConfig
    config = MediationJSONConfig.getInstance()
    config.reconfigure("tests")

    # Sample user message
    user_message = "Add to the logs of 23 December that there was no rain today"

    # Get the response from the LLM
    intent = llmhelper.get_intent(user_message)

    # Check if the response is not empty
    assert intent is not None, "LLM response should not be None"
    assert isinstance(intent, str), "LLM response should be a string"
    assert len(intent) > 0, "LLM response should not be empty"
    assert intent == "add", "Intent should be parsed as add"