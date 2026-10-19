@AGENTS.md

## Propre à Claude Code

- Les questions au propriétaire passent par `AskUserQuestion` ; le message
  final de l'agent galerie part aussi par l'outil `PushNotification`.
- Le relecteur de sécurité indépendant est un agent neuf lancé avec l'outil
  `Agent`, sans rien du contexte de la session.
