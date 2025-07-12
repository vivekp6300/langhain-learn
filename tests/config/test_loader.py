
import config.loader as loader

def test_Mediation_Config_successfully_initialized():

    # Initialize the MediationConfig
    config = loader.MediationConfig()

    # Check if the config is initialized correctly
    assert config is not None, "MediationConfig should be initialized"
    assert isinstance(config, loader.MediationConfig), "Initialized object should be of type MediationConfig"

