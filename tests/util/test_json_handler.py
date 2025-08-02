
import sys, os

print("sys.path =", sys.path)
print("cwd =", os.getcwd())

import mediation_logs.util.json_handler as json_handler


def test_Mediation_Config_successfully_initialized():

    # Initialize the MediationConfig
    config = json_handler.MediationJSONConfig.getInstance()

    # Check if the config is initialized correctly
    assert config is not None, "MediationConfig should be initialized"
    assert isinstance(config, json_handler.MediationJSONConfig), "Initialized object should be of type MediationConfig"

def test_Mediation_Logs_JSON_Loaded_successfully():

    # Load the MediationConfig
    config = json_handler.MediationJSONConfig.getInstance()
    config.reconfigure("tests")

    # Load the logs
    logs_data = config.get_all_logs()
    # Check if logs are loaded correctly
    assert logs_data is not None, "Logs should be loaded"
    assert len(logs_data) > 0, "Logs should not be empty"
    assert len(logs_data) == 4, "Logs should contain 4 entries"

def test_JSON_add_successful():

    # Load the MediationConfig
    config = json_handler.MediationJSONConfig.getInstance()
    config.reconfigure("tests")

    # Add a new log entry
    new_entry = {"period": "2023-03", "details": "New log entry"}
    config.add_or_overwrite_log(new_entry["period"], new_entry["details"])

    # Verify the new log entry is added
    logs_data = config.get_all_logs()
    assert logs_data is not None, "Logs should be loaded"
    assert len(logs_data) > 0, "Logs should not be empty"
    assert len(logs_data) == 5, "Logs should contain 5 entries"

def test_JSON_update_successful():

    # Load the MediationConfig
    config = json_handler.MediationJSONConfig.getInstance()
    config.reconfigure("tests")


    # Update an existing log entry
    period_to_update = "2023-01"
    initial_details = "Initial log entry details"
    config.add_or_overwrite_log(period_to_update, initial_details)
    updated_details = "Updated log entry details"
    assert "Log entry merged" in config.merge_log(period_to_update, updated_details), "Log update should be successful"

    # Verify the log entry is updated
    logs_data = config.get_all_logs()
    assert logs_data is not None, "Logs should be loaded"
    assert len(logs_data) > 0, "Logs should not be empty"
    
    updated_entry = config.get_log(period_to_update)
    assert updated_entry is not None, "Updated entry should exist"
    assert updated_entry ==  f"Log entry for {period_to_update} is {initial_details} {updated_details}", "Log entry details should match the updated details"
