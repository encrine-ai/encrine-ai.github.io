@AGENTS.md

## Propre à Claude Code

- Les skills sont lus dans `.claude/skills`, lien symbolique vers
  `.agents/skills` : c'est là qu'on les écrit.
- Les questions au propriétaire passent par `AskUserQuestion` ; le message
  final de l'agent galerie part aussi par l'outil `PushNotification`.
- Le relecteur de sécurité indépendant est un agent neuf lancé avec l'outil
  `Agent`, sans rien du contexte de la session.
