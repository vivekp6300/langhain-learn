
import config.loader as loader

def test_Mediation_Config_successfully_initialized():

    # Initialize the MediationConfig
    config = loader.MediationConfig.getInstance()

    # Check if the config is initialized correctly
    assert config is not None, "MediationConfig should be initialized"
    assert isinstance(config, loader.MediationConfig), "Initialized object should be of type MediationConfig"

def test_Mediation_Logs_JSON_Loaded_successfully():

    # Load the MediationConfig
    config = loader.MediationConfig.getInstance()
    config.reconfigure("tests")

    # Load the logs
    logs_data = config.mediation_logs()
    # Check if logs are loaded correctly
    assert logs_data is not None, "Logs should be loaded"
    assert len(logs_data) > 0, "Logs should not be empty"
    assert logs_data.get("entries") is not None, "Logs should contain 'entries' key"
    assert len(logs_data.get("entries")) == 4, "Logs should contain 4 entries"


