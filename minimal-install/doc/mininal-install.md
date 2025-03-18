# Minimal-install

This guide contains a step-by-step instruction how to deploy a minimal version of the TicketPilot application.
The deployment consists of tp-api (main external facing api and service registry) and an llm service holding the connection
to an azure-openai LLM deployment.

This template deployment is done via [docker compose](https://docs.docker.com/compose/) for alternative tools such as [kubernetes](https://kubernetes.io/)
there is currently no template. Simple deployments can be generated via [kompose](https://kompose.io/) otherwise you have to write your own [helm-charts](https://helm.sh/)[1].

### tp-api
An example configuration for tp-api is given in [./tp_api/.env](/minimal-install/tp_api/.env) 
Change all the instances of 'CHANGETHIS' to appropriate usernames and passwords. For the server secret key it is recommended
to use a cryptographically strong secret string e.g. via:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
API authentication is currently not supported for on-prem deployments so `DISABLE_AUTH=True`has to be set.

Once configured tp-api can be started using these commands:
```bash
 cd minimal-install/tp_api
 docker compose -f docker-compose-tp-api.yml up -d
```

Using a browser navigate to `http://'tp_base_url'/docs` to view the swagger API description of tp-api and verify that the deployment worked. Where `tp_base_url` is the URL or ip:port of your deployment.


If you plan on using [traefik](https://doc.traefik.io/traefik) for ingress you can easily do so by
- uncommenting lines 23-26 in [.env](/minimal-install/tp_api/.env) of tp-api and changing the hostname to your url
- uncommenting the traefik-labels of the 'backend' service in [docker-compose-tp-api.yml](/minimal-install/tp_api/docker-compose-tp-api.yml)

### llm-service
In [./services](/minimal-install/services) the services managed by tp-api are configured. In this case it's a single llm-service
that holds the connection to an LLM. The example .env files [llm-gpt-35-tb.env](/minimal-install/services/envs/llm-gpt-35-tb.env) and [.llm-gtp-35-tb-secrets.env](/minimal-install/services/secrets/).
Replace 'CHANGETHIS' entries according to your AzureOAI LLM deployment ('LLM_SERV_CONF_API_PREFIX' and 'LLM_TYPE' should be left as-is). Once configured the llm-service
can be started using:
```bash
 cd ../services
 docker docker compose --env-file ./compose.env -f docker-compose-llm-test.yml up -d
```

### registering the llm-service
For the system to work the llm-service service needs to be registered to tp-api. [minimal-services.yml](/minimal-install/db_conf/minimal-services.yml) contains a valid registry entry for the 'gpt-35-tb' service.
For deployments other than docker compose the url has to be changed accordingly. [register_test_services](/minimal-install/db_conf/register_test_services.py) contains a simple python
script that can be used all services listed in [minimal-services.yml](/minimal-install/db_conf/minimal-services.yml).

### testing the deployment
Finally, you can test the full deployment by issuing a simple `/chat` request using [chat_test.py](/minimal-install/chat_test.py). Make sure to adapt 'tp_url' and 'llm_service_name' if you named your service differently in [minimal-services.yml](/minimal-install/db_conf/minimal-services.yml)

### logging
if you wish to set up logging we recommend installing the [docker loki driver](https://grafana.com/docs/loki/latest/send-data/docker-driver/) and uncommenting the
relevant section in [docker-compose-tp-api.yml](/minimal-install/tp_api/docker-compose-tp-api.yml) and [docker-compose-llm-test.yml](/minimal-install/services/docker-compose-llm-test.yml).

[1]: If you have a helm deployment you are willing to share please open a PR.