# Stick Hockey Penguin TODO List

### TODO List

**1. Kärnspelmekanik:**
    *   [X] Grundläggande spelar- och bollfysik (rörelse, hopp, spark, studs)
    *   [X] Måldetektering och poängräkning
    *   [X] Match- och spelvinstlogik (först till 5 poäng/matcher)
    *   [X] Kollisionshantering (spelare-spelare, spelare-boll, boll-vägg/mark)
    *   [X] Huvudspark (Headbutt)
    *   [X] Komboräknare (airborne hits)
    *   [X] Tumble-mekanik för spelare

**2. Powerups:**
    *   [X] Powerup spawn-system (fallskärm)
    *   [X] Super Jackpot (flera powerups på en gång)
    *   Implementerade Powerups:
        *   [X] FLIGHT (vingar, flygförmåga)
        *   [X] ROCKET_LAUNCHER (raketgevär, explosioner)
        *   [X] BIG_PLAYER (större spelare)
        *   [X] SUPER_JUMP (högre hopp)
        *   [X] BALL_FREEZE (fryser bollen)
        *   [X] SPEED_BOOST (snabbare spelare)
        *   [X] GOAL_SHIELD (sköld för målet)
        *   [X] SHRINK_OPPONENT (krymp motståndare)
        *   [X] LOW_GRAVITY (lägre gravitation)
        *   [X] REVERSE_CONTROLS (omvända kontroller för motståndare)
        *   [X] ENORMOUS_HEAD (större huvud)
        *   [X] GOAL_ENLARGER (förstora motståndarens mål)
        *   [X] SWORD (svärd för spark)
            *   [X] Rita svärd
            *   [X] Svärdanimation vid spark
            *   [X] Kollision svärd-boll
            *   [X] Kollision svärd-spelare
            *   [X] Ljud för svärdsving (använder 'wall_hit' som placeholder)
            *   [-] Lägg till dedikerade svärdljud (sword_swing1.wav, sword_swing2.wav) - *Behöver ljudfiler*
            *   [-] Justera svärdets vinkel/träffyta vid behov

**3. Grafik/UI:**
    *   [X] Grundläggande spelplan (himmel, gräs, mål)
    *   [X] StickMan-rendering med animationer (gång, hopp, spark, tumble)
    *   [X] Bollrendering (fotbollsmönster)
    *   [X] Poängtavla (namn, poäng, games won)
    *   [X] Välkomstskärm
    *   [X] Game Over-skärm med trofé och vinnarbilder
    *   [X] Partikeleffekter (mål, kombo, rök från raketer, vindändring)
    *   [X] Indikatorer för aktiva powerups/status (UI nere i hörnen)
    *   [X] Skärmblixt vid mål
    *   [X] Offscreen-pil för bollen
    *   [X] Isometriska mål
    *   [X] Målsköldsgrafik med pulseffekt
    *   [X] UI-indikator för väder och dess effekter
    *   [X] UI-indikator för headbutt cooldown
    *   [X] Indikator för omvända kontroller (?)

**4. Ljud:**
    *   [X] Ljudladdningssystem
    *   [X] Grundläggande ljudeffekter (spark, hopp, studs, kollisioner etc.)
    *   [X] Målljud per spelare
    *   [X] Speaker-kösystem (för poängställning, vinnare etc.)
    *   [X] Nummerljud (0-5)
    *   [X] Ljud för "ahead" (Nils/Harry ahead)
    *   [X] Ljud för match-/gamevinst (Nils/Harry wins)
    *   [X] Ljud för Super Jackpot
    *   [X] Ljud för svärdträff (sword_hit.wav)
    *   [-] Lägg till ljud för svärdsving (se Powerups)
    *   [ ] Skapa/ersätt temporära väderljudfiler (`sunny.wav`, `rainy.wav`, etc.) med riktiga ljud. (Laddning utkommenterad tills vidare.)

**5. Vädersystem:**
    *   [X] Slumpmässigt väder per match
    *   [X] Väderpartiklar (SOL, REGN, BLÅST, SNÖ, DIMMA, GÖTEBORGSVÄDER)
    *   [X] Väderpåverkan på gravitation
    *   [X] Väderpåverkan på vind (slumpmässig styrka/riktning för BLÅST, specifik för GÖTEBORGSVÄDER)
    *   [X] Väderpåverkan på partiklar (utseende, rörelse)
    *   [X] Väderpåverkan på fysik (boll, spelare) - *Vind implementerad*
    *   [X] Dimma-overlay vid FOGGY
    *   [X] UI-indikator för väder
    *   [X] Möjlighet att byta väder med knapptryck (4)
    *   [X] Testa vädereffekter (slumpmässig vind, Göteborgsväder)

**6. Refactoring/Buggfixar:**
    *   [X] Flytta klassdefinitioner för att lösa NameError (WeatherParticle)
    *   [X] Ta bort duplicerad fysikberäkning i `Ball.update`
    *   [X] Ta bort väderberoende bollfriktion
    *   [X] Skapa `images`-mapp och flytta bilder
    *   [X] Uppdatera bildladdningsvägar
    *   [-] Undersök eventuella kvarvarande buggar eller prestandaproblem. 