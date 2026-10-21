# 30 questions techniques — Exchange

Statut : préparation d’entretien. Les commandes tenant/serveur sont des exemples non exécutés; seuls les tests hors ligne du rapport de validation ont été exécutés.

## 1. Pourquoi Exchange Server SE ?

**Question du jury :** Pourquoi Exchange Server SE ?

**Réponse technique :** C’est la voie on-premises actuellement prise en charge pour un nouveau déploiement.

**Explication détaillée :** Le support Exchange 2016/2019 est terminé depuis 2025; vérifier le build et l’OS au jour du projet.

**Exemple pratique :** Choisir SE avant de dimensionner EX01.

**Commandes pertinentes :** `Get-ExchangeServer | Select Name,AdminDisplayVersion`

**Pièges à éviter :** Installer 2019 comme nouveau standard.

**Question de relance possible :** Quel impact du modèle Subscription Edition ?

## 2. Quel est le rôle du transport ?

**Question du jury :** Quel est le rôle du transport ?

**Réponse technique :** Il soumet, catégorise, route et livre les messages.

**Explication détaillée :** Une acceptation SMTP initiale ne prouve ni catégorisation ni remise en boîte.

**Exemple pratique :** Tracer un message de RECEIVE à DELIVER.

**Commandes pertinentes :** `Get-MessageTrackingLog -MessageId <id>`

**Pièges à éviter :** S’arrêter au code SMTP 250.

**Question de relance possible :** Où trouver une file bloquée ?

## 3. Que distingue Receive et Send Connector ?

**Question du jury :** Que distingue Receive et Send Connector ?

**Réponse technique :** Le premier contrôle l’entrée; le second sélectionne les routes sortantes.

**Explication détaillée :** Bindings, authentification et permission de relais concernent le Receive Connector.

**Exemple pratique :** Tester un flux entrant puis sortant séparément.

**Commandes pertinentes :** `Get-ReceiveConnector; Get-SendConnector`

**Pièges à éviter :** Ouvrir un relais anonyme pour faire passer le test.

**Question de relance possible :** Comment limiter les IP autorisées ?

## 4. Comment éviter un relais ouvert ?

**Question du jury :** Comment éviter un relais ouvert ?

**Réponse technique :** Limiter les IP, mécanismes d’authentification et droits de relais.

**Explication détaillée :** Un connecteur trop large peut permettre l’envoi tiers et nuire à la réputation du domaine.

**Exemple pratique :** Essayer un relais non autorisé en labo.

**Commandes pertinentes :** `Get-ReceiveConnector | Format-List Name,RemoteIPRanges,PermissionGroups`

**Pièges à éviter :** Confondre réception Internet et relais arbitraire.

**Question de relance possible :** Quels journaux prouvent le refus ?

## 5. Comment diagnostiquer un utilisateur qui ne peut envoyer ?

**Question du jury :** Comment diagnostiquer un utilisateur qui ne peut envoyer ?

**Réponse technique :** Séparer client, quota, soumission, file et connecteur sortant.

**Explication détaillée :** Chaque étape a une preuve différente, à corréler par Message-ID et UTC.

**Exemple pratique :** Boîte au-dessus du seuil prohibit send.

**Commandes pertinentes :** `Get-MailboxStatistics; Get-Queue; Get-MessageTrackingLog`

**Pièges à éviter :** Augmenter le quota sans diagnostic.

**Question de relance possible :** Comment distinguer échec client et transport ?

## 6. Pourquoi un utilisateur ne reçoit-il pas ?

**Question du jury :** Pourquoi un utilisateur ne reçoit-il pas ?

**Réponse technique :** Contrôler MX, domaine accepté, Receive Connector, destinataire et livraison.

**Explication détaillée :** Le mail peut être refusé avant Exchange ou accepté puis retardé.

**Exemple pratique :** Recipient absent de la base.

**Commandes pertinentes :** `Get-AcceptedDomain; Get-Recipient; Get-MessageTrackingLog`

**Pièges à éviter :** Chercher uniquement dans Outlook.

**Question de relance possible :** Que signifie un NDR 5.x ?

## 7. Comment raisonner sur les quotas ?

**Question du jury :** Comment raisonner sur les quotas ?

**Réponse technique :** Comparer usage et seuils warning/prohibit send/prohibit receive.

**Explication détaillée :** La politique peut être héritée de la base ou propre à la boîte.

**Exemple pratique :** Une boîte atteint 1024 Mo dans le modèle.

**Commandes pertinentes :** `Get-MailboxStatistics; Get-Mailbox | Format-List UseDatabaseQuotaDefaults,*Quota*`

**Pièges à éviter :** Modifier la base pour un cas individuel sans approbation.

**Question de relance possible :** Quel impact sur l’envoi et la réception ?

## 8. Qu’est-ce qu’une mailbox database ?

**Question du jury :** Qu’est-ce qu’une mailbox database ?

**Réponse technique :** Stockage des boîtes avec journaux de transactions et état de montage.

**Explication détaillée :** La santé disque, les logs et les copies DAG influencent disponibilité et reprise.

**Exemple pratique :** DB01 sur EX01, copie optionnelle EX02.

**Commandes pertinentes :** `Get-MailboxDatabase -Status; Get-MailboxDatabaseCopyStatus`

**Pièges à éviter :** Assimiler copie DAG à sauvegarde.

**Question de relance possible :** Comment restaurer sans DAG ?

## 9. Comment fonctionne un DAG ?

**Question du jury :** Comment fonctionne un DAG ?

**Réponse technique :** Il réplique des copies de bases et permet leur activation.

**Explication détaillée :** Quorum et témoin influencent l’éligibilité; les clients nécessitent aussi un chemin d’accès disponible.

**Exemple pratique :** Bascule contrôlée DB01 vers EX02.

**Commandes pertinentes :** `Get-DatabaseAvailabilityGroup; Get-MailboxDatabaseCopyStatus`

**Pièges à éviter :** Déclarer HA avec deux VM sans tester.

**Question de relance possible :** Que se passe-t-il si le témoin est perdu ?

## 10. Pourquoi le témoin DAG ?

**Question du jury :** Pourquoi le témoin DAG ?

**Réponse technique :** Il contribue au quorum selon le nombre de membres.

**Explication détaillée :** Son placement doit être indépendant des défaillances des serveurs Exchange.

**Exemple pratique :** EX01 et EX02 avec témoin hors des deux hôtes.

**Commandes pertinentes :** `Get-DatabaseAvailabilityGroup -Status`

**Pièges à éviter :** Placer témoin et Exchange sur le même hôte physique.

**Question de relance possible :** Comment calculer le quorum ?

## 11. Comment tester une bascule DAG ?

**Question du jury :** Comment tester une bascule DAG ?

**Réponse technique :** Vérifier copies saines, lancer bascule contrôlée et mesurer service client.

**Explication détaillée :** Une copie montée sans test client ne démontre pas la continuité métier.

**Exemple pratique :** Bascule DB01 après envoi d’un message témoin.

**Commandes pertinentes :** `Move-ActiveMailboxDatabase DB01 -ActivateOnServer EX02`

**Pièges à éviter :** Tester sur production sans fenêtre ni retour arrière.

**Question de relance possible :** Comment reseeder la copie défaillante ?

## 12. Comment analyser une file en Retry ?

**Question du jury :** Comment analyser une file en Retry ?

**Réponse technique :** Examiner NextHop, LastError, DNS, TLS et journaux.

**Explication détaillée :** Une reprise aveugle de file peut masquer un problème externe persistant.

**Exemple pratique :** Smart host inaccessible.

**Commandes pertinentes :** `Get-Queue | Format-List Identity,Status,LastError,NextHopDomain`

**Pièges à éviter :** Supprimer les messages en attente.

**Question de relance possible :** Quel seuil d’alerte choisir ?

## 13. Pourquoi un certificat valide peut-il échouer ?

**Question du jury :** Pourquoi un certificat valide peut-il échouer ?

**Réponse technique :** Nom, chaîne, EKU, service binding ou FQDN du connecteur peuvent être incorrects.

**Explication détaillée :** La date seule ne prouve pas une négociation TLS réussie.

**Exemple pratique :** Certificat non lié à SMTP.

**Commandes pertinentes :** `Get-ExchangeCertificate | Format-List Subject,NotAfter,Services,Status`

**Pièges à éviter :** Remplacer le certificat sans inspecter le protocole.

**Question de relance possible :** Comment prouver la négociation TLS ?

## 14. Comment suivre un message ?

**Question du jury :** Comment suivre un message ?

**Réponse technique :** Corréler Message-ID, expéditeur, destinataire et événements sur tous les serveurs.

**Explication détaillée :** Les horodatages et l’étendue des journaux importent en multi-serveurs.

**Exemple pratique :** RECEIVE sur EX01, SEND vers le next hop.

**Commandes pertinentes :** `Get-MessageTrackingLog -MessageId <id> -Start <date>`

**Pièges à éviter :** Utiliser seulement le sujet du message.

**Question de relance possible :** Comment interpréter un événement FAIL ?

## 15. Que vaut un Test-Mailflow réussi ?

**Question du jury :** Que vaut un Test-Mailflow réussi ?

**Réponse technique :** Il vérifie un scénario de flux ciblé, pas tous les connecteurs et destinataires.

**Explication détaillée :** Il faut croiser résultat avec tracking et réception réelle.

**Exemple pratique :** Test interne EX01 vers une boîte synthétique.

**Commandes pertinentes :** `Test-Mailflow -TargetEmailAddress lab.bob@atlas.example.test`

**Pièges à éviter :** Le présenter comme preuve d’Internet mail.

**Question de relance possible :** Comment tester un domaine externe possédé ?

## 16. Comment gérer les permissions boîte ?

**Question du jury :** Comment gérer les permissions boîte ?

**Réponse technique :** Distinguer Full Access, Send As et Send on Behalf.

**Explication détaillée :** Ces droits ont des effets différents et doivent être approuvés puis audités.

**Exemple pratique :** Assistant reçoit accès lecture, pas Send As.

**Commandes pertinentes :** `Get-MailboxPermission; Get-RecipientPermission`

**Pièges à éviter :** Accorder Full Access pour envoyer au nom de.

**Question de relance possible :** Comment vérifier l’automapping ?

## 17. Quel rôle de RBAC ?

**Question du jury :** Quel rôle de RBAC ?

**Réponse technique :** Limiter commandes et portée d’administration.

**Explication détaillée :** Un rôle d’admin complet augmente le rayon d’impact; la portée doit suivre les responsabilités.

**Exemple pratique :** Opérateur des boîtes Finance uniquement.

**Commandes pertinentes :** `Get-RoleGroup; Get-ManagementRoleAssignment`

**Pièges à éviter :** Utiliser Organization Management pour tous.

**Question de relance possible :** Comment tester une restriction de scope ?

## 18. Quand utiliser un distribution group ?

**Question du jury :** Quand utiliser un distribution group ?

**Réponse technique :** Distribuer un message à des membres; pas pour porter des ACL de fichiers.

**Explication détaillée :** Propriétaire, modération et expéditeurs autorisés contrôlent l’usage.

**Exemple pratique :** Liste Operations avec modération.

**Commandes pertinentes :** `Get-DistributionGroup; Get-DistributionGroupMember`

**Pièges à éviter :** Confondre groupe de distribution et groupe de sécurité AD.

**Question de relance possible :** Comment limiter les expéditeurs externes ?

## 19. Comment protéger les adresses SMTP ?

**Question du jury :** Comment protéger les adresses SMTP ?

**Réponse technique :** Gérer domaines acceptés, politiques d’adresses et unicité.

**Explication détaillée :** Un proxyAddress dupliqué provoque un conflit de destinataire.

**Exemple pratique :** Ajouter une adresse secondaire synthétique.

**Commandes pertinentes :** `Get-Recipient -Identity a@b.example`

**Pièges à éviter :** Changer l’adresse sans vérifier les collisions.

**Question de relance possible :** Quel impact pour la réponse aux anciens messages ?

## 20. Que signifie domaine accepté ?

**Question du jury :** Que signifie domaine accepté ?

**Réponse technique :** Exchange connaît la responsabilité de routage pour ce domaine.

**Explication détaillée :** Authoritative et internal relay impliquent des décisions différentes pour les inconnus.

**Exemple pratique :** atlas.example.test en authoritative dans un labo fermé.

**Commandes pertinentes :** `Get-AcceptedDomain`

**Pièges à éviter :** Créer une route externe sans propriété du domaine.

**Question de relance possible :** Quand choisir internal relay ?

## 21. Quels prérequis AD pour Exchange ?

**Question du jury :** Quels prérequis AD pour Exchange ?

**Réponse technique :** Forêt saine, DNS, niveau/support compatibles et permissions de préparation.

**Explication détaillée :** Le setup modifie le schéma et demande une coordination forêt.

**Exemple pratique :** Tester santé DC avant préparation.

**Commandes pertinentes :** `dcdiag /e /c; repadmin /replsummary`

**Pièges à éviter :** Lancer setup sur un AD dégradé.

**Question de relance possible :** Comment revenir d’une préparation de schéma ?

## 22. Comment dimensionner Exchange ?

**Question du jury :** Comment dimensionner Exchange ?

**Réponse technique :** Utiliser la guidance actuelle, profils de charge et réserve de reprise.

**Explication détaillée :** CPU/RAM/IOPS/logs et DAG comptent; une VM minuscule n’est pas preuve production.

**Exemple pratique :** Séparer EX01/EX02 sur capacité dédiée.

**Commandes pertinentes :** `Get-MailboxDatabase -Status`

**Pièges à éviter :** Copier un chiffre de blog ancien.

**Question de relance possible :** Quel impact des logs de transport ?

## 23. Que sauvegarder ?

**Question du jury :** Que sauvegarder ?

**Réponse technique :** Bases et logs avec sauvegarde compatible Exchange, configuration et clés/certificats.

**Explication détaillée :** La restauration doit être testée; le DAG ne protège pas contre suppression logique.

**Exemple pratique :** Restaurer une boîte synthétique dans un exercice.

**Commandes pertinentes :** `Get-MailboxDatabase -Status`

**Pièges à éviter :** S’appuyer uniquement sur snapshot hyperviseur.

**Question de relance possible :** Quel RPO mesuré peut-on promettre ?

## 24. Que faire si une base échoue ?

**Question du jury :** Que faire si une base échoue ?

**Réponse technique :** Inspecter copie, disque et logs; activer copie saine ou restaurer.

**Explication détaillée :** L’ordre dépend de l’état DAG et du risque de perte de données.

**Exemple pratique :** DB01 démontée, copie EX02 saine.

**Commandes pertinentes :** `Get-MailboxDatabaseCopyStatus`

**Pièges à éviter :** Forcer le montage sans analyse.

**Question de relance possible :** Comment vérifier l’intégrité après retour ?

## 25. Quelles métriques surveiller ?

**Question du jury :** Quelles métriques surveiller ?

**Réponse technique :** Services, files, latence mail, bases, copies et certificats.

**Explication détaillée :** Un seul service Running ne mesure pas le parcours complet de message.

**Exemple pratique :** Alerte file > seuil pendant plusieurs minutes.

**Commandes pertinentes :** `Get-ServerHealth; Get-Queue`

**Pièges à éviter :** N’alerter que sur CPU.

**Question de relance possible :** Comment éviter les alertes bruitées ?

## 26. Pourquoi PowerShell 5.1 Exchange ?

**Question du jury :** Pourquoi PowerShell 5.1 Exchange ?

**Réponse technique :** Exchange utilise la version fournie avec Windows Server selon sa matrice.

**Explication détaillée :** PowerShell 7 côté poste peut servir à des outils, mais pas remplacer l’environnement Exchange requis.

**Exemple pratique :** Exécuter EMS sur serveur approuvé.

**Commandes pertinentes :** `$PSVersionTable.PSVersion; Get-ExchangeServer`

**Pièges à éviter :** Installer un WMF non pris en charge sur EX01.

**Question de relance possible :** Comment administrer à distance ?

## 27. Comment séparer hybrid et on-prem ?

**Question du jury :** Comment séparer hybrid et on-prem ?

**Réponse technique :** Définir domaines, connecteurs, identité et calendrier de migration.

**Explication détaillée :** Un tenant Exchange Online ajoute une frontière de routage et dépend des identités cohérentes.

**Exemple pratique :** Boîte pilote déplacée après validation des connecteurs.

**Commandes pertinentes :** `Get-HybridConfiguration; Get-InboundConnector`

**Pièges à éviter :** Supposer que sync AD assure le mail flow.

**Question de relance possible :** Quel outil valide la configuration hybride ?

## 28. Comment enquêter sur un service arrêté ?

**Question du jury :** Comment enquêter sur un service arrêté ?

**Réponse technique :** Confirmer état, dépendances, journaux et impact avant redémarrage.

**Explication détaillée :** Un redémarrage efface parfois le symptôme sans résoudre le crash ou manque de disque.

**Exemple pratique :** Transport arrêté sur EX01.

**Commandes pertinentes :** `Get-Service MSExchangeTransport; Get-ServerHealth`

**Pièges à éviter :** Redémarrer tous les services d’emblée.

**Question de relance possible :** Quels événements collecter avant action ?

## 29. Quelle preuve d’installation donner au jury ?

**Question du jury :** Quelle preuve d’installation donner au jury ?

**Réponse technique :** Build, OS, health, message interne tracé et capture authentique.

**Explication détaillée :** Le dépôt actuel n’a que des tests de modèle synthétique; il faut le dire clairement.

**Exemple pratique :** Montrer rapport unittest puis plan de validation SE.

**Commandes pertinentes :** `Get-ExchangeServer; Test-Mailflow`

**Pièges à éviter :** Présenter le simulateur comme livraison réelle.

**Question de relance possible :** Quelle étape débloque la preuve ?

## 30. Comment défendre le compromis sans DAG ?

**Question du jury :** Comment défendre le compromis sans DAG ?

**Réponse technique :** Un seul EX01 réduit coût mais crée un point unique de panne.

**Explication détaillée :** La disponibilité dépend alors d’un RTO de restauration mesuré, pas de la seule redondance AD.

**Exemple pratique :** Prioriser sauvegarde avant EX02 si budget réduit.

**Commandes pertinentes :** `Get-MailboxDatabase -Status`

**Pièges à éviter :** Écrire « hautement disponible » avec un serveur.

**Question de relance possible :** Comment calculer le coût du temps d’arrêt ?
