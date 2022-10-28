#!/bin/bash

aws_cli="--profile dev-admin --region us-east-1 --color on"

if [ "$1" = "list" ]; then
  aws sesv2 list-contacts $aws_cli --contact-list-name "mylist" --page-size 1000
fi

if [ "$1" = "filter" ]; then
  aws sesv2 list-contacts $aws_cli --cli-input-json file://filter_contacts.json
fi

if [ "$1" = "create" ]; then
  aws sesv2 create-contact $aws_cli --cli-input-json file://new_contact.json
fi

if [ "$1" = "update" ]; then
  aws sesv2 update-contact $aws_cli --cli-input-json file://new_contact.json
fi

if [ "$1" = "delete" ]; then
  # confirm with user
  read -p "Are you sure you want to delete $2? (y/n) " confirm
  if [ "$confirm" = "y" ]; then
    aws sesv2 delete-contact $aws_cli --contact-list-name "mylist" --email-address "$2"
  fi
fi

if [ "$1" = "get" ]; then
  aws sesv2 get-contact $aws_cli --contact-list-name "mylist" --email-address "$2"
fi
