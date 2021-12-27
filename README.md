# Backend API Challenge

## Challenge
Crear un API endpoint HTTP generico que sea capaz de filtrar, agrupar y ordenar. 


### El Dataset
El Dataset representa metricas de performance (impressions, clicks, installs, spend, revenue) para una fecha, advertising channel, country y operating system.

### Persistencia
El dataset tiene que estar alojado en una base de datos.

### Logica
el cliente de la API tiene que poder:

#### Filtrar:
```
filter by time range (date_from+date_to is enough), channels, countries, operating systems
```

#### Agrupar:
```
group by one or more columns: date, channel, country, operating system
```

#### Ordernar:
```
sort by any column in ascending or descending order
```

#### parametro en Select:
`Derived metric CPI (cost per install)` que se calcula como `cpi = spend / installs`

### Casos de uso:

##### Caso 1
Numero de impressions y clicks que ocurrieron antes del `01/06/2017` (dd/mm/yyyy), agrupado por channel y country, ordenado por clicks en orden decendente.

Ayudin:
````
1 => select channel, country, sum(impressions) as impressions, sum(clicks) as clicks from sampledataset where date < '2017-06-01' group by channel, country order by clicks desc;
2      channel      | country | impressions | clicks 
3 ------------------+---------+-------------+--------
4  adcolony         | US      |      532608 |  13089
5  apple_search_ads | US      |      369993 |  11457
6  vungle           | GB      |      266470 |   9430
7  vungle           | US      |      266976 |   7937
8  ...
````

##### Caso 2
Mostrar el numero de installs que ocurrieron en Mayo del 2017 en iOS, agrupado por `date`, ordenado por `date` de forma ascendente


##### Caso 3
Mostrar `revenue`, conseguida el `01/07/2017` para Estados Unidos (US), agrupado por `operative system` y ordenado por `revenue` en orden descendente.

##### Caso 4
Mostrar `CPI` y `spend` para Canada (CA) agrupado por `channel` ordenado por `CPI` en forma decendente. Ojo al tejo como agregas para calcular el `CPI`.

### Nota
El API endpoint debe ser capaz de servir un dataset dinamico que corresponda a cualquier combinació de filtros, agrupaciones y ordenamientos. 
No seas bobi y pases `numero de caso` como un parametro de la API.
No seas bobi y crees 4 api endpoints, te dije uno solo.

Otra vez, un solo api endpoint. Usa localhost como url para los ejemplos.

Escribilo como si el que lo fuera a leer fuera una persona mentalmente inestable con una motosierra, ademas de que tiene que poder ser mantenido por tus compañeros. Clean Code FTW.

Desde nuestro lado lo mejor es que vayas con Flask-like framework (FastAPI, Flask, etc), SQLAlchemy, SQLite, no Docker. (???)
Django va bien tambien.

Mandale a cualquier libreria third-party que haga el desarrollo mas piola vago.


## Desarrollo
Este proyecto puede ser ejecutado localmente desde la terminal, desde poetry o, como deberia ser, desde docker.

### Prerequisitos

#### FastAPI
https://fastapi.tiangolo.com
```
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
```
#### Alembic
https://github.com/sqlalchemy/alembic
```
Alembic is a database migrations tool written by the author of SQLAlchemy.
```

#### Poetry
https://python-poetry.org/docs/
```
Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.
```

#### Docker (because fuck you)
https://docs.docker.com/get-started/overview/
```
Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker’s methodologies for shipping, testing, and deploying code quickly, you can significantly reduce the delay between writing code and running it in production.
```

#### Docker compose (Because fuck you too)
https://docs.docker.com/compose/
```
Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration.
```

#### PostgreSQL
https://www.postgresql.org/
```
PostgreSQL is a powerful, open source object-relational database system with over 30 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.
```


## Docker the shit out of it
```
docker run -d --name api_db -v my_data:/var/lib/postgresql/data -p 5432:5432 -e PASTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=data_science
```

## Import the data
copy the data.txt file to the db container
```
docker cp data.txt container_name:.
```

then run the following
```
\copy analytics(date,channel,country,os,impressions,clicks,installs,spend,revenue) FROM '/data.txt' DELIMITER ',' CSV HEADER;
```

Create a new table revision by running
```
alembic revision --autogenerate -m'revision name'
```

Manually upgrade db with
```
alembic upgrade head
```

## Test this Shh
##### Caso 1
Numero de impressions y clicks que ocurrieron antes del `01/06/2017` (dd/mm/yyyy), agrupado por channel y country, ordenado por clicks en orden decendente.

```
{
  "select": "channel, country, sum(impressions) as impressions, sum(clicks) as clicks",
  "where": "date < '2017-06-01'",  
  "group_by": "channel, country",
  "order_by": "clicks desc"
}
```

```
curl -X 'POST' \
  'http://127.0.0.1:8000/analytics' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "select": "channel, country, sum(impressions) as impressions, sum(clicks) as clicks",
  "where": "date < '\''2017-06-01'\''",  
  "group_by": "channel, country",
  "order_by": "clicks desc"
}'
```

Ayudin:
````
1 => 
2      channel      | country | impressions | clicks 
3 ------------------+---------+-------------+--------
4  adcolony         | US      |      532608 |  13089
5  apple_search_ads | US      |      369993 |  11457
6  vungle           | GB      |      266470 |   9430
7  vungle           | US      |      266976 |   7937
8  ...
````

##### Caso 2
Mostrar el numero de installs que ocurrieron en Mayo del 2017 en iOS, agrupado por `date`, ordenado por `date` de forma ascendente
```
{
  "select": "date, SUM(installs) as installs",
  "where": "os='ios' AND date > '2017-05-01' AND date < '2017-06-01'",  
  "group_by": "date",
  "order_by": "date desc"
}
```

```
curl -X 'POST' \
  'http://127.0.0.1:8000/analytics' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "select": "date, SUM(installs) as installs",
  "where": "os='\''ios'\'' AND date > '\''2017-05-01'\'' AND date < '\''2017-06-01'\''",  
  "group_by": "date",
  "order_by": "date desc"
}'
```

##### Caso 3
Mostrar `revenue`, conseguida el `01/06/2017` para Estados Unidos (US), agrupado por `operative system` y ordenado por `revenue` en orden descendente.
```
{
  "select": "os, SUM(revenue) as revenue",
  "where": "country='US' AND date = '2017-06-01'",  
  "group_by": "os",
  "order_by": "revenue desc"
}
```

```
curl -X 'POST' \
  'http://127.0.0.1:8000/analytics' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "select": "os, SUM(revenue) as revenue",
  "where": "country='\''US'\'' AND date = '\''2017-06-01'\''",  
  "group_by": "os",
  "order_by": "revenue desc"
}'
```

##### Caso 4
Mostrar `CPI` y `spend` para Canada (CA) agrupado por `channel` ordenado por `CPI` en forma decendente. Ojo al tejo como agregas para calcular el `CPI`.

```
{
  "select": "channel, (SUM(spend) / SUM(installs)) as cpi",
  "where": "country='CA'",  
  "group_by": "channel",
  "order_by": "cpi desc"
}
```

```
curl -X 'POST' \
  'http://127.0.0.1:8000/analytics' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "select": "channel, (SUM(spend) / SUM(installs)) as cpi",
  "where": "country='\''CA'\''",  
  "group_by": "channel",
  "order_by": "cpi desc"
}'
```