import os
import configparser

def load_config():
    """
    Loads the project's configuration file.
    """
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'default.ini')
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        return None
    config.read(config_path)
    return config

def main():
    """
    The main execution function of the project.
    """
    print("Starting PolicyGuard...")
    
    # Load configuration
    config = load_config()
    if not config:
        return
        
    # Read a sample parameter from the config file
    project_name = config.get('project', 'name', fallback="PolicyGuard")
    version = config.get('project', 'version', fallback="0.0.1")
    
    print("-" * 30)
    print(f"Project Name: {project_name}")
    print(f"Version: {version}")
    print("Initialization successful! Your environment is ready.")
    print("Continue adding features in main.py as per your project needs.")
    print("-" * 30)
    
if __name__ == "__main__":
    main()