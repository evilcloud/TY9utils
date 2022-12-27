# install dependencies
sudo apt update
sudo apt install python3-pip -y
pip install deta

#set crontab
crontab -l > mycron
echo "* * * * * cd /home/s/TY9utils && /usr/bin/python3 d_db.py 2> err.out" > mycron
crontab mycron
rm mycron