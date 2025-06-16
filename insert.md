```sql
insert into Skills
  (name, inherit, cost_multiplier)
  
values 
    
('Broń ciężka', 'REF', 2),
('Bron długa', 'REF', 1),	
('Bron krótka', 'REF', 1),	
('Łucznictwo', 'REF', 1),	
('Ogień ciągły', 'REF', 1),	
('Atletyka', 'ZW', 1),	
('Człowiek-guma', 'ZW', 1),	
('Odporność na tortury/narkotyki', 'SW', 1),	
('Skradanie się', 'ZW', 1),	
('Taniec', 'ZW', 1),	
('Wytrwałość', 'SW', 1),	
('Biurokracja', 'INT', 1),	
('Dedukcja', 'INT', 1),	
('Hazard', 'INT', 1),	
('Język - Slang uliczny', 'INT', 1),
('Język - Niemiecki', 'INT', 1),
('Język - Polski', 'INT', 1),
('Komponowanie', 'INT', 1),	
('Kryminologia', 'INT', 1),	
('Kryptografia', 'INT', 1),	
('Księgowość', 'INT', 1),	
('Opieka nad zwierzętami', 'INT', 1),	
('Przeszukiwanie bibliotek', 'INT', 1),	
('Robienie interesów', 'INT', 1),	
('Sztuka przetrwania', 'INT', 1),	
('Taktyka', 'INT', 1),	
('Wiedza lokalna - Twoja okolica', 'INT', 1),	
('Wykształcenie', 'INT', 1),	
('Jeździectwo', 'REF', 1),	
('Pilotowanie', 'REF', 2),	
('Prowadzenie pojazdów', 'REF', 1),	
('Żegluga', 'REF', 1),	
('Czytanie z ust', 'INT', 1),	
('Koncentracja', 'SW', 1),	
('Percepcja', 'INT', 1),	
('Tropienie', 'INT', 1),	
('Ukrycie/znalezienie przedmiotu', 'INT', 1),	
('Cyberinżynieria', 'TECH', 1),	
('Elektronika i zabezpieczenia', 'TECH', 2),	
('Fałszerstwo', 'TECH', 1),	
('Fotografia/Film', 'TECH', 1),	
('Kieszonkostwo', 'TECH', 1),	
('Malowanie/Rysowanie/Rzeźba', 'TECH', 1),	
('Materiały wybuchowe', 'TECH', 2),	
('Naprawa broni', 'TECH', 1),	
('Naprawa pojazdów lądowych', 'TECH', 1),	
('Naprawa pojazdów wodnych', 'TECH', 1),	
('Naprawa statków powietrznych', 'TECH', 1),	
('Otwieranie zamków', 'TECH', 1),	
('Pierwsza pomoc', 'TECH', 1),	
('Podstawowe naprawy', 'TECH', 1),	
('Ratownictwo medyczne', 'TECH', 2),	
('Atrakcyjność', 'CHA', 1),	
('Handel', 'CHA', 1),	
('Konwersacja', 'EMP', 1),	
('Moda i styl', 'CHA', 1),	
('Odczytywanie emocji', 'EMP', 1),	
('Perswazja', 'CHA', 1),	
('Przekupstwo', 'CHA', 1),	
('Przesłuchiwanie', 'CHA', 1),	
('Znajomość półświatka', 'CHA', 1),	
('Bijatyka', 'ZW', 1),	
('Broń bała', 'ZW', 1),	
('Sztuki walki', 'ZW', 2),	
('Unik', 'ZW', 1),	
('Aktorstwo', 'CHA', 1),	
('Gra na instrumencie - Gitara elektryczna', 'TECH', 1);

update skills set inherit='ref' where inherit='REF';
update skills set inherit='int' where inherit='INT';
update skills set inherit='cha' where inherit='CHA';
update skills set inherit='tech' where inherit='TECH';
update skills set inherit='emp' where inherit='EMP';
update skills set inherit='sw' where inherit='SW';
update skills set inherit='zw' where inherit='ZW';
update skills set inherit='int' where inherit='INT';
update skills set inherit='cha' where inherit='CHA';
```

