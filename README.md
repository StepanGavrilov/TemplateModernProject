##### [![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-black.svg)](https://sonarcloud.io/summary/new_code?id=StepanGavrilov_TemplateModernProject)

[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=StepanGavrilov_TemplateModernProject&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=StepanGavrilov_TemplateModernProject)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=StepanGavrilov_TemplateModernProject&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=StepanGavrilov_TemplateModernProject)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=StepanGavrilov_TemplateModernProject&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=StepanGavrilov_TemplateModernProject)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=StepanGavrilov_TemplateModernProject&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=StepanGavrilov_TemplateModernProject)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=StepanGavrilov_TemplateModernProject&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=StepanGavrilov_TemplateModernProject)

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

