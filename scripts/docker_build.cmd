@pushd %~dp0
CALL docker build -t %IMAGE_NAME% .
@popd