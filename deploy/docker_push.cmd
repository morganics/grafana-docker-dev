@pushd %~dp0
CALL docker push %DOCKER_REPO%
@popd