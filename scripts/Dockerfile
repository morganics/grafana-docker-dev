FROM debian:jessie

RUN     apt-get update && \
        apt-get -y --no-install-recommends install libfontconfig curl ca-certificates && \
        apt-get -y install git && \
        apt-get install -y g++

RUN     curl -L https://github.com/tianon/gosu/releases/download/1.7/gosu-amd64 > /usr/sbin/gosu && \
        chmod +x /usr/sbin/gosu && \
        mkdir /usr/share/grafana-src && \
		curl -sL https://deb.nodesource.com/setup_7.x | bash - && \
		apt-get install -y nodejs && \
		curl -O https://storage.googleapis.com/golang/go1.7.5.linux-amd64.tar.gz && \
		tar -xvf go1.7.5.linux-amd64.tar.gz && \
		mv go /usr/local

EXPOSE 3000

ENV GOPATH=/usr/share/grafana-src
ENV PATH=$PATH:/usr/local/go/bin:$GOPATH/bin

RUN 	curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
		echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
		apt-get update && apt-get -y install yarn && \
		yarn install --pure-lockfile && \
		npm install -g grunt-cli && \
		go get github.com/Unknwon/bra && \
		apt-get -y install build-essential ruby-dev rubygems alien && \
		gem install fpm

#RUN 	cd /usr/share/grafana-src && \
#        go get github.com/grafana/grafana; exit 0

#RUN     cd /usr/share/grafana-src/src/github.com/grafana/grafana && \
#		go run build.go setup && \
#		go run build.go build && \
#		npm install

COPY ./run.sh /usr/share/grafana-src/run.sh
VOLUME ["/usr/share/grafana-src/src/github.com/grafana/grafana"]

WORKDIR /usr/share/grafana-src
ENTRYPOINT ["./run.sh"]



		

		
		
		
		

		
		 

