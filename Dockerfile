FROM jekyll/jekyll:4.2.0

# update bundler as verbose info crops up
RUN gem install bundler:2.3.9

ADD . /srv/jeckyll

RUN echo "Let's get to building!!!! Note this can take quite some time"
