categorias(["Accion", "RPG", "Aventura", "Casuales", "Indies", "Carreras", "Simulacion", "Deportes", "Rogue Like", "Plataformas", "Puzles", "Cartas",
"Sandbox", "Bullet Hell", "Construccion", "Ciencia Ficcion", "Pixelados", "Exploracion", "Por Turnos", "Gestion", "Shooter", "Habilidad", "Estrategia",
"Mundo Abierto", "Multijugador", "Viaje en el Tiempo", "Sigilo", "Narrativa", "Fantasia", "Fantasia Oscura", "Supervivencia", "Coleccion de Criaturas",
"Survival Horror", "Estrategia en Tiempo Real", "Lucha"]).
juego('Dark Souls', ["Accion", "RPG", "Aventura"]).
juego('Hades', ["Accion", "Indies", "Rogue Like"]).
juego('Portal', ["Puzles", "Ciencia Ficcion", "Accion"]).
juego('Stardew Valley', ["Sandbox", "Simulacion", "Gestion"]).
juego('The Binding of Isaac', ["Indies", "Rogue Like", "Accion"]).
juego('Dead Cells', ["Indies", "Rogue Like", "Accion"]).
juego('Hotline Miami', ["Accion", "Indies", "Pixelados"]).
juego('Terraria', ["Sandbox", "Aventura", "Pixelados"]).
juego('Minecraft', ["Sandbox", "Construccion", "Aventura"]).
juego('Brotato', ["Rogue Like", "Bullet Hell", "Accion"]).
juego('Downwell', ["Rogue Like", "Plataformas", "Indies"]).
juego('Bastion', ["RPG", "Accion", "Indies"]).
juego('Enter the Gungeon', ["Rogue Like", "Bullet Hell", "Accion"]).
juego('Kenshi', ["RPG", "Sandbox", "Construccion"]).
juego('Game Dev Tycoon', ["Simulacion", "Indies", "Gestion"]).
juego('Sekiro', ["Accion", "RPG", "Aventura"]).
juego('Transistor', ["Indies", "RPG", "Accion"]).
juego('Spore', ["Sandbox", "Simulacion", "Exploracion"]).
juego('Darkest Dungeon', ["RPG", "Rogue Like", "Por Turnos"]).
juego('Wizard Legend', ["Rogue Like", "Indies", "Bullet Hell"]).
juego('Forager', ["Indies", "Sandbox", "Casuales"]).
juego('Furi', ["Bullet Hell", "Accion", "Ciencia Ficcion"]).
juego('Planet Zoo', ["Simulacion", "Gestion", "Construccion"]).
juego('Pyre', ["Indies", "Deportes", "RPG"]).
juego('Children of Morta', ["Rogue Like", "Accion", "Indies"]).
juego('Graveyard Keeper', ["Indies", "Sandbox", "Gestion"]).
juego('Hand of Fate 2', ["Cartas", "Rogue Like", "Indies"]).
juego('Have a Nice Death', ["Rogue Like", "Plataformas", "Accion"]).
juego('Back to Bed', ["Puzles", "Indies", "Casuales"]).
juego('Nioh', ["RPG", "Accion", "Aventura"]).
juego('Titan Souls', ["Indies", "Bullet Hell", "Pixelados"]).
juego('Zoo Tycoon', ["Simulacion", "Gestion", "Construccion"]).
juego('Super Meat Boy Forever', ["Plataformas", "Indies", "Pixelados"]).
juego('The Legend of Zelda Ocarina of Time', ["Accion", "Aventura", "RPG"]).
juego('Super Mario Bros', ["Plataformas", "Aventura", "Accion"]).
juego('The Witcher 3 Wild Hunt', ["RPG", "Accion", "Aventura"]).
juego('Tetris', ["Puzle", "Habilidad", "Estrategia"]).
juego('The Elder Scrolls V Skyrim', ["RPG", "Accion", "Mundo Abierto"]).
juego('Red Dead Redemption 2', ["Accion", "Aventura", "Mundo Abierto"]).
juego('Grand Theft Auto V', ["Accion", "Mundo Abierto", "Aventura"]).
juego('Super Mario 64', ["Plataformas", "Aventura", "Accion"]).
juego('Halo Combat Evolved', ["Shooter", "Ciencia Ficcion", "Multijugador"]).
juego('Portal 2', ["Puzle", "Plataformas", "Accion"]).
juego('Chrono Trigger', ["RPG", "Viaje en el Tiempo", "Aventura"]).
juego('Metal Gear Solid', ["Accion", "Sigilo", "Narrativa"]).
juego('Mass Effect 2', ["RPG", "Ciencia Ficcion", "Accion"]).
juego('Super Smash Bros Ultimate', ["Lucha", "Multijugador", "Accion"]).
juego('Final Fantasy VII', ["RPG", "Fantasia", "Aventura"]).
juego('Bloodborne', ["Accion", "RPG", "Fantasia Oscura"]).
juego('The Legend of Zelda Breath of the Wild', ["Accion", "Aventura", "Mundo Abierto"]).
juego('Half-Life 2', ["Shooter", "Ciencia Ficcion", "Accion"]).
juego('Super Metroid', ["Accion", "Plataformas", "Aventura"]).
juego('Overwatch', ["Shooter", "Multijugador", "Accion"]).
juego('Diablo II', ["RPG", "Accion", "Fantasia"]).
juego('Super Mario World', ["Plataformas", "Aventura", "Accion"]).
juego('Resident Evil 4', ["Survival Horror", "Accion", "Aventura"]).
juego('Fallout New Vegas', ["RPG", "Mundo Abierto", "Accion"]).
juego('The Last of Us', ["Accion", "Aventura", "Supervivencia"]).
juego('Pokemon Red/Blue', ["RPG", "Coleccion de Criaturas", "Aventura"]).
juego('StarCraft', ["Estrategia en Tiempo Real", "Ciencia Ficcion", "Multijugador"]).
juego('Castlevania Symphony of the Night', ["Accion", "Plataformas", "Aventura"]).

recuperar_categorias(Juego, Categorias) :-
    juego(Juego, Categorias).

%con findall busca todos los juegos que cumplen que Lista sea sublista de Categoria con el forall y el member, y esos juegos los guarda en Resultado. 
recuperar_juegos_con_categorias(Lista, Resultado) :-
    findall(Juego, (
        juego(Juego, Categorias),
        forall(member(Categoria, Lista), member(Categoria, Categorias))
    ), Resultado).
