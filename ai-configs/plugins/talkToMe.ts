export const TalkToMe = async ({ project, client, $, directory, worktree }) => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.idle") {
        return "Use the `echo '{message to user}' | kokoro-tts` to tell the user that you are done working on what he had instructed you. Keep it short and simple. He just needs to be notified. Thats all"
      }
    },
  }
}