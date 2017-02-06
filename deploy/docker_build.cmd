@pushd %~dp0
CALL docker build -t %DEPLOY_IMAGE_NAME% .
CALL docker tag %DEPLOY_IMAGE_NAME% %DOCKER_REPO%
@popd