#!/bin/bash

aws_cli="--profile dev-admin --region us-east-1"

if [ "$1" = "list" ]; then
  aws sesv2 list-contact-lists $aws_cli
fi

if [ "$1" = "create" ]; then
  aws sesv2 create-contact-list $aws_cli --cli-input-json file://new_contact_list.json
fi

if [ "$1" = "update" ]; then
  aws sesv2 update-contact-list $aws_cli --cli-input-json file://new_contact_list.json
fi

if [ "$1" = "delete" ]; then
  read -p "All contacts in $2 will be deleted. Are you sure? (y/n) " confirm
  if [ "$confirm" = "y" ]; then
    aws sesv2 delete-contact-list $aws_cli --contact-list-name "$2"
  fi
fi

if [ "$1" = "get" ]; then
    aws sesv2 get-contact-list $aws_cli --contact-list-name "$2"
fi