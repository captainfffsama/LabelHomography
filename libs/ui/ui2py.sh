ls|grep .ui|awk -F. '{print $1}'|xargs -I {} pyuic5 {}.ui -o Ui_{}.py
