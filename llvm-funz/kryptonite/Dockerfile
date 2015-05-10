#
#    Dockerfile Spartacus -
#    Copyright (C) 2015 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    overclok@wildout:~/dev$ mkdir kryptonite && cd kryptonite
#    overclok@wildout:~/dev/kryptonite$ sudo docker build --tag=kryptonite .
#    [...]
#    Successfully built bf9140f60d0a
#    overclok@wildout:~/dev/kryptonite$ sudo docker images
#    REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
#    kryptonite          latest              b97b2d28f05e        13 seconds ago      954.6 MB
#    overclok@wildout:~/dev/kryptonite$ sudo docker run -ti kryptonite /bin/bash
#    [...]

FROM ubuntu:14.04
MAINTAINER Axel "0vercl0k" Souchet <0vercl0k[at]tuxfamily[dot]org>

#
# Basics
#
COPY config/baseline-ubuntu.sh /tmp
RUN bash /tmp/baseline-ubuntu.sh && rm /tmp/baseline-ubuntu.sh

#
# scripts
#
USER over
WORKDIR /home/over
RUN mkdir scripts
WORKDIR /home/over/scripts
## TV show downloader
RUN wget https://raw.githubusercontent.com/0vercl0k/TV-Show-Downloader/master/run_tvshow_downloader.sh > /dev/null 2>&1
RUN wget https://raw.githubusercontent.com/0vercl0k/TV-Show-Downloader/master/tvshow_downloader.py > /dev/null 2>&1
COPY config/tvshow_downloader.cfg /home/over/scripts
## Webpage changes tracker
RUN wget https://raw.githubusercontent.com/0vercl0k/stuffz/master/webpage_changes_tracker.py > /dev/null 2&1
COPY config/urls_to_track /home/over/scripts
COPY config/email_account.cfg /home/over/scripts

#
# crontab
#
USER over
## crontab.fifteen-min
WORKDIR /home/over
COPY config/crontab.fifteen-min /home/over
## master user crontab
WORKDIR /tmp
RUN echo '*/15 * * * * /home/overclok/scripts/master.sh' > overcron && crontab overcron && rm overcron
WORKDIR /home/over

