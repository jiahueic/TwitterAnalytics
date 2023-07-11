FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 python3-venv cron
RUN mkdir /root/mastadon_script
COPY mastadon_script /root/mastadon_script
WORKDIR /root/mastadon_script
RUN python3 -m venv /root/mastadon_script/venv/
RUN chmod +x /root/mastadon_script/requirementsinstall.sh
RUN /bin/bash -c "/root/mastadon_script/requirementsinstall.sh"

# Set the entrypoint to the interactive script
ENTRYPOINT ["/bin/bash", "-c", "chmod +x /root/mastadon_script/start.sh && /root/mastadon_script/start.sh"]

CMD tail -f /dev/null
