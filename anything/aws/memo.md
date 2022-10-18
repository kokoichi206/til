## ssh

ダウンロードしたキー（下では mine.pem）を 700 にする

ssh -i /Users/kokoichi/Downloads/me.pem ec2-user@18.144.152.182

sudo apt install postfix
sudo systemctl enable postfix
sudo systemctl start postfix

curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.rpm.sh | sudo bash

sudo EXTERNAL_URL="https://gitlab.example.com" yum install -y gitlab-ee

sudo EXTERNAL_URL="http://18.144.152.182/gitlab" yum install -y gitlab-ee

vi /etc/gitlab/gitlab.rb

sudo gitlab-ctl reconfigure
