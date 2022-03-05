# GWAS Pipeline User and Setup Guide (release 1)

## Introduction

This guide covers the basic functionality and setup of a project for the GWAS pipeline. The GWAS pipeline searches a database of associations using a trait ID or trait name to return an annotated table of associations and a list of unique variants. An LD score is then calculated between the unique variants and a supplied mTAG output for a specified reference population to return a table of the highest $R^2$ values in the LD matrix.

> Note: `Release 1` is implemented using `Python 3.10`.

## Configuration

### Global Application Settings

The application setup is configured in the `app_config.yml` config file which resides in `/global_config/`. 

**`app_config.yml`**

```yaml
associations:
	api: gwas_catalog
	p_value: 5x10^-8
ld:
	api: ld_link
	ref_pop: 
```

1. **`associations::api`**: name of the API to search for associations (valid APIs are enumerated in `/domain/enums/associations_api_type`)
2. **`associations::p_value`**:
3. **`ld::api`**: name of the API to calculate LD score (valid APIs are enumerated in `/domain/enums/ld_api_type`)
4. **`ld::ref_pop`**:

### API-Specific Settings

Based on the selected APIs in `app_config.yml`,  `key:value` mappings to access data fields are loaded from API-specific config files located in `/global_config/`.

For example, **`gwas_catalog_config.yml`**:

```yaml
base_url: https://www.ebi.ac.uk/gwas/rest/api/
trait_code_url: efoTraits/search/findByEfoTrait?trait={}
associations_url: efoTraits/{}/associations?projection=associationByEfoTrait
valid_bases: ACTG?
efo_traits: _embedded/efoTraits
trait_code: _embedded/efoTraits/0/shortForm
associations: _embedded/associations
p_value: pvalue
...
```

## Running GWAS Pipeline

The pipeline is executed through `python gwas_pipeline.py` with the following arguments. Either an  `id` or `name` must be provided. 

`-id`						search for associations based on trait ID code

`-n, --name`		searched for associations based on trait name.

`-o, --output`	file path for save outputs (project folder)

## Software Architecture



## Logging

The application setup is configured in the `log_config.yml` config file which resides in `/global_config/`.  This configuration typically does not require any modification unless changes to the default logging levels are required or other more advanced settings like logging formats, etc.

**`log_config.yml`**

```yaml
formatters:
  basic:
    datefmt: '%Y-%m-%d %H:%M:%S'
    format: '{asctime:s}:{levelname:s}:{name:s}:{message:s}'
    style: '{'
  control:
    format: '{message:s}'
    style: '{'
  verbose:
    datefmt: '%Y-%m-%d %H:%M:%S'
    format: '{asctime:s}:{levelname:s}:{name:s}:{lineno:d}:{message:s}'
    style: '{'
handlers:
  console:
    class: logging.StreamHandler
    formatter: control
    stream: ext://sys.stderr
loggers:
  gwas_pipeline:
    handlers:
    - console
    level: INFO
version: 1
```
