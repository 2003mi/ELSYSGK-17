# ELSYSGK-17
Dette er koden til lys boksen.

Den mest relevante kode filene er trukket ut, men vist man vil finne ein fullstendig kopi av alt som er på raspberry pien så finner man det i [e.zip](https://github.com/2003mi/ELSYSGK-17/blob/main/e.zip)

## Setup 
1. Set opp ein normal raspberry pi og ssh deg inn på han.
1. sørg for python3 er installert.
1. Installer rpi_ws281x med commandoen ```pip3 install rpi_ws281x ```

## Auto kjør

Det er viktig at koden kjører som andimistrator når man åpnar han, eller så vil han ikkje fungere.
For å starte han på startup så lagde vi run.sh og start.sh scripten

run.sh er den som vi starter opp når vi raspberry pien får straum, det er mange forkjelige måter å gjere dette på. Det man må sørgje for er at scripten kjører med sudo privliages når han starter opp ellers så vil han ikkje fungere.
Man må også laste ned screen for at coden skal kjøre i bakgrunnen ```sudo apt install screen```

Vi brukte rc.local for å kjøre scripten på startup, men det er bare å endre på pathen i scripten og så kjøre run.sh gjennom han. Eg skriver ikkje korleis man gjer det siden den finnes ein haug med andre tutorials korleis man gjer det som [denne](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/).
