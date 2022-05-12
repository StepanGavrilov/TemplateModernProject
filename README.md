=======
Start local
==================

    rm -rf .env && ./docker/env.sh Local >> .env && poetry run ./docker/api/api.sh

Start local (docker)
==================

    rm -rf .env && ./docker/env.sh Development >>.env && docker-compose -f docker-compose.yml up --build

Mirror gitlab
==================
[GitLab Mirror](https://gitlab.com/GavrilovStepan01/TemplateModernProject)

