FROM sounddr-env:latest

WORKDIR /

#RUN apt-get update
#
#RUN apt-get install 'ffmpeg'\
#    'libsm6'\
#    'libxext6'  -y

ENV PATH /opt/conda/envs/SoundDr-BE/bin:$PATH

COPY . .

RUN /bin/bash -c "source activate SoundDr-BE" || true

CMD [ "python", "run.py" ]