import os
import click
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
from datetime import datetime

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
@click.option('--input-file', '-i', required=True, type=click.Path(exists=True, dir_okay=False), help='Path to the input CSV file.')
@click.option('--output-file', '-o', type=click.Path(dir_okay=False), help='Path to save the output CSV file. [Optional]')
@click.option('--policy', '-p', required=True, type=click.Path(exists=True, dir_okay=False), help='Path to the moderation policy file.')
@click.option('--text-column', '-c', required=True, type=str, help='The name of the column containing the text to moderate.')
def process(input_file, output_file, policy, text_column):
    """
    Process a CSV file against a moderation policy and save the results.
    """
    click.echo("🚀 Initializing PolicyGuard...")

    # --- 1. Setup and Validation ---
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.secho("Error: OPENAI_API_KEY not found in .env file.", fg='red')
        return
    click.secho("✅ OpenAI API key loaded.", fg='green')

    try:
        loaded_policy = load_and_validate_policy(policy)
        click.secho(f"✅ Policy '{loaded_policy['name']}' loaded and validated.", fg='green')
    except PolicyError as e:
        click.secho(f"Error loading policy: {e}", fg='red')
        return

    # --- 2. Read and Prepare Data ---
    try:
        df = pd.read_csv(input_file)
        if text_column not in df.columns:
            click.secho(f"Error: Text column '{text_column}' not found in the input file.", fg='red')
            return
        click.secho(f"✅ Input file '{input_file}' loaded. Found {len(df)} records.", fg='green')
    except Exception as e:
        click.secho(f"Error reading CSV file: {e}", fg='red')
        return

    # --- 3. Core Processing Loop with Progress Bar ---
    results = []
    click.echo("⏳ Starting moderation process...")
    
    # tqdm creates the progress bar
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Moderating"):
        text_to_check = str(row[text_column])
        
        if pd.isna(text_to_check) or not text_to_check.strip():
            result = {'flagged': False, 'reason': 'empty_text', 'details': ''}
        else:
            result = moderate_text(text_to_check, loaded_policy)
        
        # Combine original row data with moderation results
        output_row = row.to_dict()
        output_row.update(result)
        results.append(output_row)

    # --- 4. Save Results ---
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(input_file).replace('.csv', '')
        output_file = os.path.join('output', f"{base_name}_results_{timestamp}.csv")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    
    click.secho(f"✅ Processing complete. Results saved to '{output_file}'", fg='green')


if __name__ == '__main__':
    cli()