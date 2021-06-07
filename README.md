# Hercules

**Hercules** to system rozliczeń dla wirtualnych firm (grup graczy), którzy grają w grę Euro Truck Simulator 2. Służy on do zliczania ilości przejechanych kilometrów, dodawania nowych tras, sprawdzania aktywności *kierowców* i wiele innych rzeczy mających urealnić rozgrywkę.

**Link do projektu**: [https://hercules-project.herokuapp.com/panel](https://hercules-project.herokuapp.com/panel)

![https://i.imgur.com/9Ecs5z0.png](https://i.imgur.com/9Ecs5z0.png)

### Założenia projektu

Projekt Hercules został stworzony w czerwcu 2020 roku, był to mój pierwszy projekt w Django. Miał on służyć społeczności graczy Euro Truck Simulator 2 głównie poprzez innowacyjną funkcję opartą na OCR, która ze screenshota podsumowania trasy pobierała i przetwarzała automatycznie dane, dodając trasę do systemu, unikając żmudnych prac wpisywania każdej informacji.

Projekt został wydany w wersji beta i doczekał się prawie 300 stałych użytkowników, w tym około 20 wirtualnych firm. Ze względu na brak opcji na rozwój i pojawiające się nowe obowiązki projekt został zawieszony. 

### Stack technologiczny

Cały projekt oparty jest na frameworku **Django**. Za rozpoznawanie znaków odpowiada biblioteka **pytesseract**, która jest interfejsem dla aplikacji **Tesseract**. Aby usprawnić wszelakie procesy związane z zadaniami, użyte jest **Celery**, a jego brokerem jest **Redis**. Frontend oparty jest na **SCSS/SASS**, głównie na frameworku **Bulma**. 

### Funkcje projektu

Główną funkcją projektu było **dodawanie i rozliczanie tras w sposób zautomatyzowany** z użyciem Tesseracta. *Szef* firmy sprawdzał poprawność zrzutu ekranu z treścią wpisaną do systemu i zatwierdzał bądź odrzucał trasy, które zostały nadesłane przez *kierowców*. Prócz tego system posiada automatyczną *Giełdę zleceń*, której zlecenia generowane są cyklicznie co 30 minut. System sprawdza też z użyciem oficjalnego API TruckersMP ilość graczy na poszczególnych serwerach trybu wieloosobowego gry.

Cały projekt miał docelowo doczekać się aplikacji napisanej w języku C#, która poprzez API dodawałaby nowe trasy bezpośrednio z gry, bez konieczności logowania się do systemu, jednak ze względu na zawieszenie projektu, nie udało się tego zrealizować.

W systemie jest założone konto demonstracyjne, z którego można skorzystać do samodzielnego przetestowania i sprawdzenia możliwości Herculesa. 

**Login**: demo_driver

**Hasło:** tUTzSycixRSP8Fi
