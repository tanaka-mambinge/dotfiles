import type { Plugin } from "@opencode-ai/plugin";

const SKILL_SEARCH_PROMPT = `
<skill_search>
Before starting ANY task, you MUST check if you've already searched for relevant skills in this conversation. 
If skills haven't been discovered yet, immediately search using the skill tool for: language/framework patterns, architecture preferences, code standards, style conventions, domain guidelines, and project practices.
Load and thoroughly review all applicable skill documentation that matches your task.
Anchor your entire implementation in these discovered skills and established patterns—this guarantees consistency and prevents reinventing solutions.
Never proceed with coding or planning until skill discovery is complete.
</skill_search>`;

export const ForceSkillSearchPlugin: Plugin = async (ctx) => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.created") {
      }
    },
    "experimental.chat.system.transform": async (input, output) => {
      // Inject skill search instruction into the beginning of every session
      output.system.push(SKILL_SEARCH_PROMPT);
    },
  };
};
