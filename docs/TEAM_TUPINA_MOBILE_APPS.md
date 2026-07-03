# Team Tupina: Android e iOS

## Objetivo

Preparar o app mobile do ecossistema Team Tupina usando o app Flutter do wger como base, conectado ao backend wger personalizado.

## O que ja esta pronto

- App Flutter baixado em `mobile/team-tupina-app`.
- Android application id configurado como `br.com.teamtupina.app`.
- iOS bundle id configurado como `br.com.teamtupina.app`.
- Nome exibido configurado como `Team Tupina` / `Team Tupiná`.
- Cores principais alteradas para a identidade visual Team Tupina.
- Icones, logo e splash substituidos por assets Team Tupina.
- Servidor padrao parametrizado por `TEAM_TUPINA_SERVER_URL`.
- Scripts de checagem, execucao local e build Android adicionados em `scripts/mobile`.

## Status tecnico validado em localhost

Backend local em `http://127.0.0.1:8002`:

- `GET /api/v2/` respondeu 200.
- `GET /api/v2/version/` respondeu 200 com `2.6.0a2`.
- `GET /api/v2/min-app-version/` respondeu 200 com `1.11.0`.
- `GET /api/v2/powersync-token` ainda respondeu 404.

Flutter SDK nao esta instalado no PATH desta maquina no momento, entao ainda nao foi possivel compilar o APK/AAB localmente.

## Modo local de teste

Enquanto PowerSync nao estiver publicado no backend local, use o modo API-only:

```powershell
.\scripts\mobile\run-android-local.ps1
```

Este script usa:

```text
TEAM_TUPINA_SERVER_URL=http://10.0.2.2:8002
TEAM_TUPINA_REQUIRE_POWERSYNC=false
```

`10.0.2.2` e o endereco que o Android Emulator usa para acessar o localhost da maquina host.

Para celular fisico:

```powershell
$env:TEAM_TUPINA_SERVER_URL = 'http://IP_DA_MAQUINA:8002'
.\scripts\mobile\run-android-local.ps1
```

## Build Android de producao

Requisitos:

- Flutter SDK 3.10+.
- Android Studio.
- Android SDK.
- JDK.
- Keystore de release.
- Conta Google Play Console.

Comando:

```powershell
.\scripts\mobile\build-android-release.ps1 -ServerUrl https://app.teamtupina.com.br
```

Saida esperada:

```text
mobile/team-tupina-app/build/app/outputs/bundle/release/app-release.aab
```

## Build iOS de producao

Requisitos:

- macOS.
- Xcode.
- CocoaPods.
- Flutter SDK 3.10+.
- Apple Developer Program.
- Bundle id `br.com.teamtupina.app` criado no Apple Developer.
- App cadastrado no App Store Connect.

Comando no macOS:

```bash
cd mobile/team-tupina-app
flutter pub get
flutter build ipa --release \
  --dart-define=TEAM_TUPINA_SERVER_URL=https://app.teamtupina.com.br \
  --dart-define=TEAM_TUPINA_REQUIRE_POWERSYNC=true
```

## Requisitos para publicar nas lojas

- Dominio publico com HTTPS: exemplo `https://app.teamtupina.com.br`.
- `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` configurados no backend.
- SMTP funcional para e-mails.
- Storage persistente para media.
- Backups automaticos de banco e media.
- Politica de privacidade publicada.
- Termos de uso publicados.
- E-mail de suporte.
- Screenshots Android e iOS.
- Declaracoes de privacidade da Google Play e App Store.
- PowerSync ativo se o build for publicado com `TEAM_TUPINA_REQUIRE_POWERSYNC=true`.

## PowerSync obrigatorio para producao completa

O app mobile do wger usa PowerSync para banco local, cache offline e sincronizacao. Para producao, implementar e validar:

- `GET /api/v2/powersync-token`
- `PUT/PATCH/DELETE /api/v2/upload-powersync-data`
- `GET {POWERSYNC_URL}/probes/liveness`
- JWT de curta duracao para conexao PowerSync
- Regras de permissao por usuario
- Teste de login, sync inicial, edicao offline e reenvio online

## Decisao pendente de repositorio

O app em `mobile/team-tupina-app` ainda e um reposititorio Git separado, clonado do upstream Flutter do wger. Antes de fazer o primeiro release oficial, escolher:

- submodulo Git, mantendo atualizacoes upstream mais claras;
- codigo vendorizado, removendo o `.git` interno e versionando tudo dentro do reposititorio Team Tupina.
