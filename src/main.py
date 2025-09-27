import os
import click
from dotenv import load_dotenv
from src.policy_loader import load_and_validate_policy, PolicyError
from src.core_engine import moderate_text

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

    click.echo("-----------------------------------------")
    
    # 3. Process the input file
    try:
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                text_to_check = line.strip()
                if not text_to_check:
                    continue

                click.echo(f"Checking line {i+1}: \"{text_to_check}\"")
                result = moderate_text(text_to_check, loaded_policy)
                
                if result['flagged']:
                    click.secho(f"  -> FLAGGED. Reason: {result['reason']}. Details: {result['details']}", fg='yellow')
                else:
                    click.secho(f"  -> OK. Reason: {result['reason']}.", fg='green')
                    
    except Exception as e:
        click.secho(f"An error occurred while processing the file: {e}", fg='red')

    click.echo("-----------------------------------------")
    click.echo("✅ Processing complete.")


if __name__ == '__main__':
    cli()