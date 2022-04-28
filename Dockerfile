ARG BASE_IMAGE_NAME=teampicnic/picnic-python-base
ARG BASE_IMAGE_VERSION=3.0.0

### Stage to build Python environment.
# Use a build stage to prevent exposing Nexus credentials in the final image.
FROM $BASE_IMAGE_NAME:$BASE_IMAGE_VERSION as build

ARG NEXUS_USERNAME
ARG NEXUS_PASSWORD
RUN : "${NEXUS_PASSWORD:?Build argument NEXUS_PASSWORD is mandatory} \
    ${NEXUS_USERNAME:?Build argument NEXUS_USERNAME is mandatory}"

COPY Pipfile Pipfile.lock ./
RUN pipenv sync

### Stage to run the application.
FROM $BASE_IMAGE_NAME:$BASE_IMAGE_VERSION

# Make sure image version is passed to the project as an environment variable.
ARG IMAGE_VERSION
ENV IMAGE_VERSION=$IMAGE_VERSION

ARG PROJECT_SLUG
RUN : "${PROJECT_SLUG:?Build argument PROJECT_SLUG is mandatory.}"
# Assign the argument to an environment variable to be able to use it in ENTRYPOINT.
ENV PROJECT_SLUG $PROJECT_SLUG

# Get the environment built by `build` stage.
COPY --from=build $WORK_DIR/.venv .venv
COPY --from=build $WORK_DIR/Pipfile $WORK_DIR/Pipfile.lock ./

COPY $PROJECT_SLUG $PROJECT_SLUG

# Run the application.
ENTRYPOINT ["pipenv", "run", "python", "-m", "$PROJECT_SLUG"]
