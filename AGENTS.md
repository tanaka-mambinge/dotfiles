# Question Tool Usage Guidelines

## Core Principle

Use the question tool with multiple choice options instead of open-ended questions. Users prefer clicking over typing.

## Question Rounds

You have a **maximum of 3 question rounds** to gather all necessary information. Each round should:

- Ask multiple related questions efficiently
- Anticipate details the user may not have considered
- Include clarifying questions for ambiguous requirements
- Gather architectural, technical, and implementation preferences

Plan your questions strategically across the rounds to collect comprehensive information without back-and-forth inefficiency.

## Question Format

### Always Structure Questions As

```
Question: [Clear, concise question]
Options:
1. [Option 1]
2. [Option 2]
3. [Option 3]
4. [Option 4]
5. Other (let me specify)
```

### Key Rules

- **3-5 options per question** - Enough choice without overwhelming
- **Last option is always "Other"** - Allows custom input when needed
- **Concise and distinct options** - Easy to scan and select
- **Multiple choice by default** - Only use manual input when explicitly requested

## What to Ask About

Use your judgment to determine what's most relevant, but consider:

- Technical stack and tooling preferences
- Architecture and project structure
- Database and state management
- Authentication and security requirements
- API design and validation patterns
- Error handling and logging approach
- Testing and deployment preferences
- Performance and scalability concerns
- Edge cases and constraint handling

## Examples

**Good - Multiple Choice:**

```
Question: How should we handle authentication?
Options:
1. JWT tokens
2. Session-based with cookies
3. OAuth2 with third-party providers
4. No authentication needed
5. Other (let me specify)
```

**Avoid - Open-ended:**

```
How should we handle authentication?
```

## When Manual Input is Acceptable

- User explicitly requests to type a detailed response
- Question requires unique, complex answer that can't be templated
- Follow-up clarification on a custom "Other" response

**Remember:** Make selections fast and easy. The goal is to gather maximum information with minimum typing.
