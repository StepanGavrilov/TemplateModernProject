Start local (docker)
==================

    rm -rf .env && ./docker/env.sh Development >>.env && docker-compose -f docker-compose.yml up --build

Api start local
==================

    sudo kill -9 $(lsof -t -i:9999) && ./docker/env.sh Local >> .env && ./docker/api/api.sh Local

Mirror gitlab
==================
[GitLab Mirror](https://gitlab.com/GavrilovStepan01/TemplateModernProject)

Stats
==================
<img src="coverage-badge.svg" alt="coverage">
<img src="tests-badge.svg" alt="tests">
<img src="flake8-badge.svg" alt="flake8">

