# MERITO_26

Dokumentacja aktualnego stanu projektu POC z asystentem biznesowym opartym o Streamlit, OpenRouter i mikroserwisy danych.

## Opis projektu

Aplikacja realizuje prosty przeplyw czatu z routingiem intencji:
1. Uzytkownik loguje sie i wysyla wiadomosc.
2. Orchestrator buduje kontekst i wysyla zapytanie do LLM.
3. LLM zwraca JSON z decyzja routingu.
4. Dla trasy mikroserwisowej uruchamiany jest mikroserwis plikowy lub SQL.
5. Wynik mikroserwisu wraca do kolejnego przebiegu LLM i do UI.

Glowny entrypoint aplikacji:
- llm/llmFrontApp.py

## Quick Start

### Wymagania

- Python 3.10+
- Dostep do bazy PostgreSQL (np. Supabase)
- Klucz API OpenRouter

### Instalacja

1. Zainstaluj zaleznosci:

```bash
pip install -r requirements.txt
```

2. Przygotuj plik srodowiskowy dla aplikacji:

```bash
cp .env_example .env
```

3. Uzupelnij wymagane zmienne w .env:
- DATABASE_URL
- OPENROUTER_API_KEY
- OPENROUTER_MODEL
- OPENROUTER_BASE_URL

### Uruchomienie

```bash
streamlit run llm/llmFrontApp.py
```

Domyslny testowy login w UI:
- Tester

## Struktura projektu

```text
llm/
  llmFrontApp.py
  requirements.txt
  src/
    chat/
      chatOrchestrator.py
      userValidation.py
      modelRouting.py
    config/
      llmConfig.py
      llmConfig.json
      microservices.json
      appConfig.md
    connectors/
      llm_connector.py
      db_connector.py
    microservices/
      microServiceManager.py
      read_services.py
```

## Architektura i role modulow

### UI i sesja

- llm/llmFrontApp.py
- Odpowiada za logowanie, stan sesji i renderowanie rozmowy w Streamlit.

### Orkiestracja czatu

- llm/src/chat/chatOrchestrator.py
- Odpowiada za handshake, wywolanie LLM, parsowanie JSON i routing.

### Walidacja uzytkownika

- llm/src/chat/userValidation.py
- Laduje liste dozwolonych uzytkownikow z llm/src/config/llmConfig.json.

### Kontekst i kontrakt LLM

- llm/src/config/llmConfig.py
- Definiuje zasady i strukture JSON odpowiedzi wykorzystywanej do routingu.

### Integracja z LLM

- llm/src/connectors/llm_connector.py
- Realizuje polaczenie z OpenRouter Chat Completions i handshake modelu.

### Mikroserwisy i dane

- llm/src/microservices/microServiceManager.py
- llm/src/microservices/read_services.py
- llm/src/connectors/db_connector.py

Zakres:
- mikroserwisy plikowe (CSV/JSON),
- mikroserwisy SQL z konfiguracji,
- konwersja danych do formy przekazywanej do LLM i UI.

## Konfiguracja

### Zmienne srodowiskowe

Przyklad znajduje sie w .env_example.

- DATABASE_URL: connection string do PostgreSQL
- OPENROUTER_API_KEY: klucz API do OpenRouter
- OPENROUTER_MODEL: nazwa modelu (np. nvidia/nemotron-3-super-120b-a12b:free)
- OPENROUTER_BASE_URL: endpoint API (domyslnie https://openrouter.ai/api/v1)

### Konfiguracja aplikacyjna

- llm/src/config/llmConfig.json
  - lista allowedUsers (np. Tester, Patryk, admin)
- llm/src/config/microservices.json
  - definicje i aktywnosc mikroserwisow SQL
  - przyklad aktywnej uslugi: turnover_by_city

## Katalog mikroserwisow

Mikroserwisy aktualnie obslugiwane przez manager:

- read_json
  - zrodlo: llm/pliki testowe/testing_json.json
- read_csv
  - zrodlo: llm/pliki testowe/triage_csv.csv
- turnover_by_city
  - zrodlo: SQL z llm/src/config/microservices.json
  - wykonanie: przez llm/src/connectors/db_connector.py

## Przeplyw aplikacji

1. Logowanie w UI i walidacja uzytkownika.
2. Handshake modelu LLM.
3. Przyjecie wiadomosci i wywolanie LLM z dodatkowym kontekstem.
4. Odczyt decyzji routingu z JSON.
5. (Opcjonalnie) wykonanie mikroserwisu.
6. Drugi przebieg LLM na danych z backendu.
7. Prezentacja odpowiedzi w UI.

## Troubleshooting

- Brak OPENROUTER_API_KEY:
  - handshake i wywolania chat nie powioda sie.
- Brak DATABASE_URL:
  - polaczenie SQL nie zostanie nawiazane.
- Bledny format odpowiedzi LLM:
  - orchestrator przejdzie na fallback conversation.

## Znane ograniczenia POC

- modelRouting.py jest placeholderem i nie bierze udzialu w aktywnym flow.
- appConfig.md jest obecnie pusty.
- W psycopg 3.3.4 moze pojawiac sie ostrzezenie typowania dla row_factory=dict_row; nie wplywa to na runtime.
