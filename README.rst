Start local
==================
.. code-block:: shell
    rm -rf .env && ./docker/env.sh Local >> .env && poetry run ./docker/api/api.sh

Start local (docker)
==================
.. code-block:: shell
    rm -rf .env && ./docker/env.sh Development >>.env && docker-compose -f docker-compose.yml up --build

Mirror gitlab
==================
https://gitlab.com/GavrilovStepan01/awesomeproject1