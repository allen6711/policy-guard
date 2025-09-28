import os
from openai import OpenAI

# Initialize the OpenAI client
# It will automatically read the OPENAI_API_KEY from the environment
client = OpenAI()

def moderate_text(text: str, policy: dict) -> dict:
    """
    Moderates a single piece of text based on the provided policy.

    Args:
        text: The text to moderate.
        policy: The loaded policy dictionary.

    Returns:
        A dictionary containing the moderation result.
    """
    # 1. Rule-Based Filtering
    for rule in policy.get('rules', []):
        if rule['type'] == 'keyword':
            for keyword in rule['value']:
                if keyword.lower() in text.lower():
                    return {
                        'flagged': True,
                        'reason': 'keyword_match',
                        'details': f"Matched keyword: '{keyword}'"
                    }

    # 2. LLM Analysis (if not caught by rules)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": policy['llm_prompt']},
                {"role": "user", "content": text}
            ],
            max_tokens=10,
            temperature=0.0
        )
        llm_result = response.choices[0].message.content.strip().lower()

        if 'flag' in llm_result:
            return {
                'flagged': True,
                'reason': 'llm_flagged',
                'details': f"LLM response: '{llm_result}'"
            }
        else:
            return {
                'flagged': False,
                'reason': 'llm_ok',
                'details': f"LLM response: '{llm_result}'"
            }

    except Exception as e:
        # Added a fallback if the client failed to initialize despite the fix
        if not client:
            return {
                'flagged': False,
                'reason': 'client_not_initialized',
                'details': 'OpenAI client failed to initialize. Skipping LLM check.'
            }
        return {
            'flagged': False,
            'reason': 'api_error',
            'details': f"An error occurred with the OpenAI API: {e}"
        }