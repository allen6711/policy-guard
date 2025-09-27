import os
import click
from dotenv import load_dotenv
from src.policy_loader import load_and_validate_policy, PolicyError

# Load environment variables from .env file
load_dotenv()

@click.group()
def cli():
    """
    PolicyGuard: An LLM-powered moderation tool.
    """
    pass

@cli.command()
@click.option('--file', '-f', required=True, type=click.Path(exists=True), help='Path to the data file to process.')
@click.option('--policy', '-p', required=True, type=click.Path(exists=True), help='Path to the moderation policy file.')
def process(file, policy):
    """
    Process a file against a moderation policy.
    """
    click.echo("🚀 Initializing PolicyGuard...")

    # 1. Verify API Key is loaded
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.secho("Error: OPENAI_API_KEY not found in .env file.", fg='red')
        return
    click.secho("✅ OpenAI API key loaded successfully.", fg='green')

    # 2. Load and validate the policy
    try:
        loaded_policy = load_and_validate_policy(policy)
        click.secho(f"✅ Successfully loaded and validated policy: '{loaded_policy['name']}'", fg='green')
    except PolicyError as e:
        click.secho(f"Error loading policy: {e}", fg='red')
        return

    click.echo(f"Processing file: {file}")
    click.echo("-----------------------------------------")
    # In future parts, we will add the core logic here.
    click.echo("🚧 Part 2 setup complete. The application can now load and validate policies.")


if __name__ == '__main__':
    cli()