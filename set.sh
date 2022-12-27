# install dependencies
sudo apt update
sudo apt install python3-pip -y
pip install deta


# checking for DETA_KEY environment variable
if [[ -z "${DETA_KEY}" ]]; then
  MY_SCRIPT_VARIABLE="DETA_KEY is not available. Aborting..."
else
  #set crontab
    crontab -l > mycron
    echo "* * * * * cd /home/s/TY9utils && /usr/bin/python3 d_db.py 2> err.out" > mycron
    crontab mycron
    rm mycron
fi