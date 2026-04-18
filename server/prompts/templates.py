"""Prompt Templates for MCP Server"""
from typing import Any


class PromptTemplates:
    """Collection of prompt templates"""

    @staticmethod
    def get_code_review_prompt(language: str = "Python") -> dict[str, Any]:
        """Code review prompt template"""
        return {
            "name": "code_review",
            "description": f"Review {language} code for best practices and issues",
            "arguments": [
                {
                    "name": "code",
                    "description": "The code to review",
                    "required": True
                },
                {
                    "name": "language",
                    "description": "Programming language",
                    "required": False
                }
            ],
            "prompt": f"""Please review the following {language} code:

{{{{code}}}}

Focus on:
1. Code quality and best practices
2. Potential bugs or issues
3. Performance considerations
4. Security vulnerabilities
5. Readability and maintainability

Provide specific suggestions for improvement."""
        }

    @staticmethod
    def get_sql_helper_prompt() -> dict[str, Any]:
        """SQL query helper prompt template"""
        return {
            "name": "sql_helper",
            "description": "Help write SQL queries",
            "arguments": [
                {
                    "name": "description",
                    "description": "Description of what the query should do",
                    "required": True
                },
                {
                    "name": "schema",
                    "description": "Database schema information",
                    "required": False
                }
            ],
            "prompt": """Help me write a SQL query based on the following:

Description: {{description}}

{% if schema %}
Database Schema:
{{schema}}
{% endif %}

Please provide:
1. The SQL query
2. Explanation of how it works
3. Any potential performance considerations"""
        }

    @staticmethod
    def get_system_diagnostics_prompt() -> dict[str, Any]:
        """System diagnostics prompt template"""
        return {
            "name": "system_diagnostics",
            "description": "Diagnose system issues",
            "arguments": [
                {
                    "name": "issue",
                    "description": "Description of the system issue",
                    "required": True
                }
            ],
            "prompt": """Help diagnose the following system issue:

{{issue}}

Please provide:
1. Possible causes
2. Diagnostic steps
3. Recommended solutions
4. Prevention strategies"""
        }

    @staticmethod
    def get_api_integration_prompt() -> dict[str, Any]:
        """API integration helper prompt template"""
        return {
            "name": "api_integration",
            "description": "Help integrate with APIs",
            "arguments": [
                {
                    "name": "api_name",
                    "description": "Name of the API",
                    "required": True
                },
                {
                    "name": "task",
                    "description": "What you want to do with the API",
                    "required": True
                }
            ],
            "prompt": """Help me integrate with the {{api_name}} API to {{task}}.

Please provide:
1. Required authentication setup
2. Example code for the integration
3. Error handling best practices
4. Rate limiting considerations"""
        }

    @staticmethod
    def list_all_prompts() -> list[dict[str, Any]]:
        """List all available prompts"""
        return [
            PromptTemplates.get_code_review_prompt(),
            PromptTemplates.get_sql_helper_prompt(),
            PromptTemplates.get_system_diagnostics_prompt(),
            PromptTemplates.get_api_integration_prompt()
        ]
