# Read the configuration files and load them to the required fields
config_location = 'config.json'
with open(config_location, 'r') as f:
    config = json.loads(f.read())