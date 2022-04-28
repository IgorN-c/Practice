# practice-dwh

Practicing fetching from picnics data warehouse using python.

## Running the project

### Running `practice_dwh` locally

Launch the main functionality, by running in the project root:

```shell
$ pipenv sync
$ pipenv run python -m practice_dwh
```

> Note: Environment variables can be injected into the containers using `.env` file in
> the root of the project. Use `.env.example` as a base for your `.env` file, adding any
> needed environment variable.

> Note 2: `NEXUS_USERNAME`, `NEXUS_PASSWORD` and `EXAMPLE_PASSWORD` must be defined in
> the environment for the above commands to run.

## Testing and documenting the code

> Note: this part requires running `pipenv sync --dev` to install the dev dependencies.

### Running `pytest` test cases

To run the unit tests defined in the `tests` folder, in the project root run:

```shell
$ pipenv run guide test
```
