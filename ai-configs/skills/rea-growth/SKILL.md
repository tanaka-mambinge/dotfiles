---
name: rea-growth
description: Reverse engineer how a company gets users, identify its growth and content patterns, and turn public evidence into practical experiments. Use for growth teardowns, competitor distribution research, or brand content analysis.
---

# REA growth

Research a company from public evidence and explain its growth mechanics in a useful, reproducible playbook. This skill works with the assistant's built-in web search and page-reading tools; it does not require Treg or another external service.

## Modes

- **Growth teardown** (default): how a company grew, how it gets users, or what to adapt.
- **Content review**: what a company's public posts look and sound like, and which visible patterns repeat.

## Cost and access rules

- Use built-in web search and page opening/extraction tools, plus pages anyone can view without an account.
- Do not install or invoke Treg, paid APIs, metered data providers, scraping services, or paid trials. Do not ask the user to create an account, add a payment method, or provide credentials.
- Do not bypass sign-in, paywalls, rate limits, or anti-bot controls. If a source is blocked or unavailable, say so and continue with other public evidence.
- Do not contact people, submit forms, create accounts, or interact with the target's product as a user.
- Keep research spend on external data services at $0. A suggested experiment may have costs; state those separately and include a no-spend way to test it.

## Evidence rules

- Mark claims **SEEN** when a linked public source directly shows them. Mark **INFERRED** when reasoning from linked evidence, and state the reasoning.
- Link each material finding to its source. Prefer the company's own site, newsroom, product documentation, public launch posts, and official social accounts for first-party facts; use credible reporting and public registries for outside confirmation.
- Distinguish the date an event happened from the date a page or article was published. For current claims, check the page and report the access date.
- Never invent traffic, conversion, customer, revenue, ranking, ad-spend, engagement, or growth numbers. Use a number only when a public source gives it, and label estimates as estimates.
- A search result sample is not a complete channel audit. A missing result does not prove that a company does not use a channel.
- Treat timing as correlation, not proof of cause. Say when public evidence cannot establish causation.

## Inputs

The target name or domain is required. If the user has not named one, ask for it before researching. The user's company, domain, stage, country, and audience are optional: use them to tailor recommendations when supplied, but do not block a general teardown when they are absent. Do not assume the user is a direct competitor.

## Growth teardown workflow

Research only as deeply as needed to answer the request. Use several focused searches, then follow the most useful first-party and credible sources.

1. **Offer and activation.** Read the target's homepage, product/about pages, pricing, templates or use cases, help/onboarding docs, changelog, and public partner pages when available. Note who it serves, the promise, free and paid boundaries, signup friction that is publicly documented, first-use guidance, integrations, and anything users can share with non-users. Do not start signup.
2. **Timeline.** Find dated launches, major product changes, funding, partnerships, public user/customer/revenue milestones, and notable distribution campaigns. Verify important milestones from primary sources or reliable reporting. Build a short timeline; do not claim an inflection if the public record does not support one.
3. **Acquisition and distribution.** Check public evidence for search and evergreen pages, paid ads through free public ad libraries when accessible, founder/company content, press and creator coverage, communities, partnerships, and product-sharing loops. Link representative examples. Clearly label inaccessible ad libraries or social pages as unavailable; absence of visible ads is not evidence of no advertising.
4. **Content patterns** (when relevant). Identify official public accounts from links on the company's own site. Review a bounded sample of accessible posts, state the sample size and date range, and compare visible engagement only within the same platform. Describe repeated hooks, formats, topics, and calls to action. Do not claim a winning format from a tiny or biased sample; do not describe images or videos that you could not inspect.
5. **Growth model.** Connect the evidence into a simple path: discovery → signup → first value → payment (if publicly documented) → sharing/return use. For each step, separate what is directly documented from what is inferred. Explain which mechanisms plausibly reinforce one another and what remains unknown.
6. **Practical plays.** Give up to ten experiments, ordered by evidence strength and relevance. For each include: the mechanism, evidence link, why it may transfer, a small test, a success metric, effort, and a no-spend version. If the user's company or stage is unknown, write recommendations for a clearly named generic company type or offer to tailor later; never pretend to know the user's business.

## Content review workflow

- Sample accessible official posts across the requested channels, preferably recent posts with enough time to gather visible engagement. State the channels, sample sizes, date range, and access date.
- Summarize recurring topics, hooks, formats, calls to action, posting cadence where observable, and visual style only when the media itself is visible.
- Link the example posts. Compare engagement within each platform only; avoid calling a pattern from too few examples.
- If the user provides their own company and audience, turn supported patterns into example hooks and one practical post brief. Otherwise keep the output focused on the target.

## Output

For a growth teardown, respond with:

1. A concise read on the growth model.
2. The offer and activation path.
3. A dated timeline of supported milestones.
4. Channel evidence and product loops, grouped by what is actually visible.
5. The strongest supported growth mechanisms, clearly marked SEEN or INFERRED.
6. Practical experiments with evidence, effort, metric, and no-spend option.
7. Evidence gaps and a short method note, including that no paid data services were used.

For a content review, report sample and dates, recurring patterns, linked examples, what cannot be concluded, and (when company context was provided) adaptable examples.

Create a separate Markdown, HTML, or CSV file only when the user asks for a file or the task clearly calls for a deliverable artifact.
