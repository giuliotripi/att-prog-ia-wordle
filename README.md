# Attività progettuale di Intelligenza Artificiale M

Questo repository contiene il sorgente dell'attività progettuale di IA,
che consiste nell'implementazione di una IA in grado di giocare al gioco Wordle

All'interno della cartella dictionaries sono presenti l'elenco delle parole utilizzate,
divise per lingua.

Il numero di parole presenti nel file è particolarmente importante nel determinare quanto spesso
l'AI sarà in grado di indovinare la parola corretta

## Esecuzione

Nel repository sono presenti 3 eseguibili:
- il server di gioco che sceglie la parola;
- il client che si occupa di indovinare la parola scelta dal server;
- una utility che suggerisce all'utente quali parole utilizzare nel gioco reale.

Per avviare il server:

```bash
python3 server.py
```

Per avviare il client:
```bash
python3 client.py <language> <word_length>
```

Per avviare il suggeritore:
```bash
python3 prompter.py <language> <word_length>
```

Per effettuare più test è possibile lanciare il file `executor.py` senza argomenti, che esegue più volte il client
scrivendo in un file csv i risultati delle varie esecuzioni

Nel file `base.py` sono contenute tutte le funzioni di utilità utilizzare dai due esecutori.