# From https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04

# If you update your Django application, you can restart the Gunicorn process to pick up the changes by typing:

`sudo systemctl restart gunicorn`
If you change Gunicorn socket or service files, reload the daemon and restart the process by typing:
`sudo systemctl restart gunicorn.socket gunicorn.service`
`sudo systemctl daemon-reload`

# If you change the Nginx server block configuration, test the configuration and then Nginx by typing:

sudo nginx -t && sudo systemctl restart nginx

# Logs

Check the Nginx process logs by typing: `sudo journalctl -u nginx`
Check the Nginx access logs by typing: `sudo less /var/log/nginx/access.log`
Check the Nginx error logs by typing: `sudo less /var/log/nginx/error.log`
Check the Gunicorn application logs by typing: `sudo journalctl -u gunicorn`
Check the Gunicorn socket logs by typing:` sudo journalctl -u gunicorn.socket`

# When updating domain:
`sudo rsubl /etc/nginx/sites-available/medusa_website`
`sudo systemctl reload nginx`
