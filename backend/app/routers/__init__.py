ImportError: no se puede importar el nombre 'presupuestos' desde 'app.routers' (/app/app/routers/__init__.py)
Rastreo (última llamada más reciente):
  Archivo "/app/.venv/bin/uvicorn", línea 7, en <module>
    sys.exit(principal())
             ~~~~^^
  Archivo "/app/.venv/lib/python3.13/site-packages/click/core.py", línea 1485, en __call__
    devuelve self.main(*args, **kwargs)
    )
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  Archivo "/app/.venv/lib/python3.13/site-packages/click/core.py", línea 1406, en main
    devolver ctx.invoke(self.callback, **ctx.params)
    rv = self.invoke(ctx)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  Archivo "/app/.venv/lib/python3.13/site-packages/click/core.py", línea 1269, en invocar
  Archivo "/app/.venv/lib/python3.13/site-packages/click/core.py", línea 824, en invocar
    ...<45 líneas>...
        h11_max_incomplete_event_size=h11_max_incomplete_event_size,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ^^^^
    ~~~^
        aplicación,
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/main.py", línea 412, en main
    devolver devolución de llamada (*args, **kwargs)
    correr(
    ^
    ~~~~~~~~~~~^^
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/config.py", línea 435, en carga
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/main.py", línea 579, en ejecución
    self.loaded_app = importar_desde_cadena(self.app)
    servidor.run()
    ~~~~~~~~~~^^
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/server.py", línea 66, en ejecución
  Archivo "/mise/installs/python/3.13.12/lib/python3.13/asyncio/runners.py", línea 195, en ejecución
    devolver runner.run(principal)
    devolver asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~^^^^^^
  Archivo "/mise/installs/python/3.13.12/lib/python3.13/asyncio/runners.py", línea 118, en ejecución
    esperar self._serve(sockets)
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/server.py", línea 77, en _serve
    configuración.load()
    devolver self._loop.run_until_complete(tarea)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  Archivo "uvloop/loop.pyx", línea 1518, en uvloop.loop.Loop.run_until_complete
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/server.py", línea 70, en el servidor
                      ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
  Archivo "<frozen importlib._bootstrap>", línea 1331, en _find_and_load_unlocked
  Archivo "<frozen importlib._bootstrap>", línea 935, en _load_unlocked
  Archivo "<frozen importlib._bootstrap_external>", línea 1023, en exec_module
  Archivo "<frozen importlib._bootstrap>", línea 488, en _call_with_frames_removed
  Archivo "/app/main.py", línea 9, en <module>
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/importer.py", línea 19, en import_from_string
    módulo = importlib.import_module(module_str)
    desde app.routers importar auth, cedis, scorecards, presupuestos, documentos
  Archivo "/mise/installs/python/3.13.12/lib/python3.13/importlib/__init__.py", línea 88, en import_module
    devolver _bootstrap._gcd_import(nombre[nivel:], paquete, nivel)
ImportError: no se puede importar el nombre 'presupuestos' desde 'app.routers' (/app/app/routers/__init__.py)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Rastreo (última llamada más reciente):
  Archivo "<frozen importlib._bootstrap>", línea 1387, en _gcd_import
  Archivo "/app/.venv/bin/uvicorn", línea 7, en <module>
  Archivo "<frozen importlib._bootstrap>", línea 1360, en _find_and_load
    sys.exit(principal())
             ~~~~^^
  Archivo "/app/.venv/lib/python3.13/site-packages/click/core.py", línea 1485, en __call__
    ~~~^
        aplicación,
        ^^^^
    ...<45 líneas>...
        h11_max_incomplete_event_size=h11_max_incomplete_event_size,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/main.py", línea 579, en ejecución
    servidor.run()
    ~~~~~~~~~~^^
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/server.py", línea 66, en ejecución
    devolver asyncio.run(self.serve(sockets=sockets))
    devuelve self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  Archivo "/app/.venv/lib/python3.13/site-packages/click/core.py", línea 1406, en main
    rv = self.invoke(ctx)
  Archivo "/app/.venv/lib/python3.13/site-packages/click/core.py", línea 1269, en invocar
    devolver ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  Archivo "/app/.venv/lib/python3.13/site-packages/click/core.py", línea 824, en invocar
    devolver devolución de llamada (*args, **kwargs)
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/main.py", línea 412, en main
    correr(
    ~~~~~~~~~~~^^
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/config.py", línea 435, en carga
    self.loaded_app = importar_desde_cadena(self.app)
                      ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/importer.py", línea 19, en import_from_string
    módulo = importlib.import_module(module_str)
  Archivo "/mise/installs/python/3.13.12/lib/python3.13/importlib/__init__.py", línea 88, en import_module
    devolver _bootstrap._gcd_import(nombre[nivel:], paquete, nivel)
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  Archivo "/mise/installs/python/3.13.12/lib/python3.13/asyncio/runners.py", línea 195, en ejecución
    devolver runner.run(principal)
           ~~~~~~~~~~^^^^^^
  Archivo "/mise/installs/python/3.13.12/lib/python3.13/asyncio/runners.py", línea 118, en ejecución
    devolver self._loop.run_until_complete(tarea)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  Archivo "uvloop/loop.pyx", línea 1518, en uvloop.loop.Loop.run_until_complete
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/server.py", línea 70, en el servidor
    esperar self._serve(sockets)
  Archivo "/app/.venv/lib/python3.13/site-packages/uvicorn/server.py", línea 77, en _serve
    configuración.load()
